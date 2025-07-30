# activitypub-linked-data

**Local JSON-LD context loader and RDF namespace definitions for
ActivityPub and the Fediverse**

`activitypub-linked-data` is a Python utility package that provides
preloaded JSON-LD context documents and RDF namespace constants for
use in ActivityPub implementations and other Fediverse-compatible
applications. It includes a built-in JSON-LD document loader optimized
for speed, reliability, and offline use.

## Features

- Local resolution of common JSON-LD context URLs used in the
  Fediverse
- Built-in `rdflib` namespaces for ActivityStreams, Security and
  Identity vocabularies
- Secure document loader to replace remote HTTP fetching
- Compatible with `rdflib` and `pyld` JSON-LD processing
- Designed for use in Fediverse applications, including servers and
  identity tools

---

## Installation

```sh
pip install activitypub-linked-data
```


## Usage

```python
from pyld import jsonld

from ap.linked_data import AS2, setup_rdflib_local_handler, jsonld_local_document_loader

if __name__ == '__main__':
    setup_rdflib_local_handler() # Patches rdflib to use locally defined contexts, when available.

    # Sets up jsonld to use local context documents
    jsonld.set_document_loader(jsonld_local_document_loader)

    # Use a namespace
    print(AS2.Person)  # -> https://www.w3.org/ns/activitystreams#Person
```

Note: pyld is not declared as a dependency. You need to include in your own project if you
wish to use `jsonld_local_document_loader`

## Attribution

This package is derived from the
[Takahē](https://github.com/jointakahe/takahe) project, which is
licensed under the [BSD 3-Clause
License](https://opensource.org/licenses/BSD-3-Clause).
