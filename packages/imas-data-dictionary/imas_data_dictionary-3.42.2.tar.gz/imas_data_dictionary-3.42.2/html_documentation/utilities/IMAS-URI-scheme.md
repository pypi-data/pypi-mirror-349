# IMAS Access-Layer URI Scheme Documentation 

- Version: 0.3 
- Date: 21 November 2022


## Background

Historically, identification of IMAS data-entries (also referred to as _data source_ or simply _resource_ in this document) 
with the Access-Layer is defined by 5 arguments:

- **`shot`** (int)
- **`run`** (int)
- **`user`** (string)
- **`database`** (string)
- **`version`** (string)

When more storage backends have been implemented in the Access-Layer, the **`backendID`** (int) was added to the list.
This fixed list imposed some limitations (ranges of `shot` and `run`) and required implicit rules to convert them into 
a standardized path on the system. It also lacks the flexibility asked for by developers (e.g capability to store data 
in non-standard paths had to be added by _hacking_ the interpretation of the `user` argument with additional rules to
cover cases where an absolute path is given).

To address some of the limitation and improve the flexibility and genericity of the identification of IMAS data resources, 
a proposal (initially discussed in [IMAS-1281](https://jira.iter.org/browse/IMAS-1281)) was made to introduce a new API taking a URI as argument. 
This document describes the chosen URI schema.


## IMAS URI structure

The chosen IMAS data source is following the general idea from URI standard definition from [RFC-3986](https://www.rfc-editor.org/rfc/rfc3986.html)
but is not aiming at being publickly registered. For reference, the general URI structure is the following: `scheme:[//authority]path[?query][#fragment]`.

For sake of clarity and coherence, it was decided to define a single unified `scheme` for IMAS data resources (named `imas`)
instead of defining different scheme for each backend. This implies that the backend needs to be specified in another manner.
We opt for using the `path` part of the URI to specify the backend.

As a result, the structure of the IMAS URI is the following, with elements between square brackets being optional:

**`imas:[//host/]backend?query[#fragment]`**

Each part of the URI are described in more details in the following subsections.


### Scheme

For consistency, the scheme is simply named `imas` and followed by `:` that separates the scheme from the next parts 
(either the `host` or the `backend`). 

### Host  

The host (which takes place of the authority in general URI syntax) allows to specify the address 
of the server on which the data is located (or accessed through). The `host` starts with a double slash `//` (similarily 
to the standard authority it is contextually replacing) and ends with a single slash `/` (which is a difference with 
the authority syntax, as it is missing otherwise a delimiter with the next contextual element since `backend` replaces `path`).

The structure of the `host` is **`//[user@]server[:port]/`**, where:

- **`user`** is the username which will be recognized on the server to authenticate the submitter to this request. 
This information is optional, for instance for if the authentication is done by other means (e.g. using PKI certificates in the 
case of UDA) or if the data server does not require authentication;
- **`server`** is the address of the server (typically the fully qualified domain name or the IP of the server);
- **`port`** is optional and can be used to specify a port number onto which sending the requests to the server.

When the data is stored locally the `host` (localhost) is omitted. 

Example: a `host` would typically be the address of a UDA server, with which the UDA backend of the Access-Layer
will send requests for data over the netwrok. A URI would then look like: `imas://uda.iter.org/uda?...`.

### Backend

The `backend` is the name of the Access-Layer backend used to retrieve the stored data, this name is given in lower case and is mandatory.
Current possibilities are: `mdsplus`, `hdf5`, `ascii`, `memory` and `uda`. Be aware that some backends may not be available in a given install of the Access-Layer.

### Query

A `query` is mandatory. It starts with `?` and is composed of a list of semi-colon `;` (or ampersand `&`) separated pairs `key=value`. The following keys are standard and recognized by all backends:

- `path`: absolute path on the localhost where the data is stored;
- `shot`, `run`, `user`, `database`, `version`: allowed for compatibility purpose with legacy data-entry identifiers.

**Note**: if legacy identifiers are provided, they are always transformed into a standard `path` before the query is being passed to the 
backend.

Other keys may exist, be optional or mandatory for a given backend. Please refer to the latest documentation of the Access-Layer for more information on backend-specific keys.

### Fragment

In order to identify a subset from a given data-entry, a `fragment` can be added to the URI. 
Such `fragment`, which starts with a hash `#`, is optional and allows to identify a specific IDS, or a part of an IDS. 

The structure of the fragment is **`#idsname[:occurrence][/idspath]`**, where:

- **`idsname`** is the type name of the IDS, given in lower case, is mandatory in fragments and comes directly after the `#` delimiter;
- **`occurrence`** is the occurrence of the IDS (refer to the [Access-Layer User Guide](https://user.iter.org/?uid=YSQENW&action=get_document) for more information), is optional and comes after a colon `:` delimiter that links the occurrence to the IDS specified before the delimiter;
- **`idspath`** is the path from IDS root to the IDS subset that needs to be identified, and is optional (in such case the fragment identifies the entire IDS structure). Refer to the [IDS path syntax](IDS-path-syntax.md) document for more information.



