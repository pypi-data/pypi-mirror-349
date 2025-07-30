import http.client
import json
import logging
from io import BytesIO
from urllib import parse
from urllib.request import (
    HTTPHandler,
    HTTPSHandler,
    OpenerDirector,
    Request,
    install_opener,
)
from urllib3.response import HTTPResponse

from .contexts import SCHEMA_DEFINITIONS


logger = logging.getLogger(__name__)


def jsonld_local_document_loader(url: str, options={}):
    pieces = parse.urlparse(url)
    try:
        assert pieces.hostname is not None
        key = pieces.hostname + pieces.path.rstrip("/")
        if key not in SCHEMA_DEFINITIONS:
            key = "*" + pieces.path.rstrip("/")
        return SCHEMA_DEFINITIONS[key]
    except AssertionError:
        logger.info(f"No host name for json-ld schema: {url!r}")
        return SCHEMA_DEFINITIONS["unknown"]
    except KeyError:
        logger.info(f"Ignoring unknown json-ld schema: {url!r}")
        return SCHEMA_DEFINITIONS["unknown"]


class LocalDocumentHandler(HTTPHandler, HTTPSHandler):
    """
    A HTTP handler that to get context documents directly, instead
    of loading from the web every time.
    """

    PROTECTED_URLS = [
        "www.w3.org/ns/activitystreams",
        "w3id.org/security/v1",
        "w3id.org/security",
        "w3id.org/identity/v1",
        "www.w3.org/ns/did/v1",
        "w3id.org/security/data-integrity/v1",
        "w3id.org/security/multikey/v1",
        "joinmastodon.org/ns",
        "funkwhale.audio/ns",
        "schema.org",
        "purl.org/wytchspace/ns/ap/1.0",
    ]

    @property
    def document_definitions_by_url(self):
        return {url: SCHEMA_DEFINITIONS[url]["document"] for url in self.PROTECTED_URLS}

    def _response_from_local_document(self, req, document) -> HTTPResponse:
        # See https://github.com/getsentry/responses/blob/master/responses/__init__.py
        # https://github.com/getsentry/responses/issues/691

        data = BytesIO()
        data.close()
        headers = {"Content-Type": "application/ld+json"}

        orig_response = HTTPResponse(
            body=data,
            msg=headers,
            preload_content=False,
        )
        status = 200

        body = BytesIO()
        body.write(json.dumps(document).encode("utf-8"))
        body.seek(0)

        return HTTPResponse(
            status=status,
            reason=http.client.responses.get(status, None),
            body=body,
            headers=headers,
            original_response=orig_response,
            preload_content=False,
            request_method=req.get_method(),
        )

    def http_open(self, req: Request) -> http.client.HTTPResponse:
        url = req.get_full_url().removeprefix("http://")
        document = self.document_definitions_by_url.get(url)

        if document is not None:
            return self._response_from_local_document(req, document)
        return super().http_open(req)

    def https_open(self, req: Request) -> http.client.HTTPResponse:
        url = req.get_full_url().removeprefix("https://")

        document = self.document_definitions_by_url.get(url)
        if document is not None:
            return self._response_from_local_document(req, document)

        return super().https_open(req)


def setup_rdflib_local_handler():
    opener = OpenerDirector()
    opener.add_handler(LocalDocumentHandler())
    install_opener(opener)


__all__ = ["jsonld_local_document_loader", "setup_rdflib_local_handler"]
