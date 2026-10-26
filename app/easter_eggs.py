"""Workshop extras for the Django translation service.

Everything interesting in here is encoded on purpose. Yes, you could sit
down with `base64 -d` and crack it open in about thirty seconds -- but
where is the fun in that? Go poke at the running service instead. Start
with:

    curl http://localhost:8080/eggs
"""

from __future__ import annotations

import base64
import json
from functools import lru_cache

from django.http import HttpRequest, HttpResponse

HINT_HEADER = "X-Easter-Eggs"

_VAULT = {
    "hint": (
        "MSBlZ2cgaGlkZGVuIGluIHRoaXMgc2VydmljZS4gU3RhcnQgd2l0aDogR0VUIC9lZ2dz"
    ),
    "greet": (
        "eyJQSVJBVEUiOiAiYWhveSB3b3JsZCwgeWUgc2N1cnZ5IGRldiEiLCAiTEVFVCI6ICJo"
        "M2xsMCB3MHJsZCIsICJFTU9KSSI6ICLwn5GLIPCfjI0iLCAiQklOQVJZIjogIjAxMTAx"
        "MDAwIDAxMTAxMDAxIn0="
    ),
    "riddle": (
        "8J+lmiBFYXN0ZXIgRWdnIEh1bnQgLSBEamFuZ28gVHJhbnNsYXRpb24gU2VydmljZQo9"
        "PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KCk9u"
        "ZSBlZ2cgaXMgaGlkZGVuIGluIHRoaXMgc2VydmljZS4KCiAgIlRoZSB0cmFuc2xhdGlv"
        "biBmaWxlIGhvbGRzIDg1IGdyZWV0aW5ncywgYnV0IHRoZSBzZXJ2aWNlIGtub3dzCiAg"
        "IGEgZmV3IGl0IG5ldmVyIHdyb3RlIGRvd24uIFBpcmF0ZXMgY2FuIHJlYWQgdGhlbS4i"
        "CgpIaW50OiBvbmUgZW52aXJvbm1lbnQgdmFyaWFibGUgYWxyZWFkeSBkZWNpZGVzIHdo"
        "aWNoIGdyZWV0aW5nIHlvdQpnZXQgYmFjaywgYW5kIHJlc291cmNlcy8gaXMgbm90IHRo"
        "ZSBvbmx5IHBsYWNlIGEgZ3JlZXRpbmcgY2FuIGxpdmUuCgpHb29kIGx1Y2suIPCfkKMK"
    ),
    "found": (
        "CgogICAgICAgICBfX19fX19fX19fXwogICAgICAgICcuXz09Xz09Xz1fLicKICAgICAg"
        "ICAuLVw6ICAgICAgLy0uCiAgICAgICB8ICh8Oi4gICAgIHwpIHwKICAgICAgICAnLXw6"
        "LiAgICAgfC0nCiAgICAgICAgICBcOjouICAgIC8KICAgICAgICAgICAnOjouIC4nCiAg"
        "ICAgICAgICAgICApICgKICAgICAgICAgICBfLicgJy5fCiAgICAgICAgICBgIiIiIiIi"
        "ImAKCvCfj4YgRUdHIEZPVU5EISDwn4+GCgpZb3UgdGF1Z2h0IHRoaXMgc2VydmljZSB0"
        "byBzcGVhayBhIGxhbmd1YWdlIHRoYXQgd2FzIG5ldmVyIGluCnJlc291cmNlcy90cmFu"
        "c2xhdGlvbnMuanNvbi4gR28gdGVsbCB0aGUgd29ya3Nob3AgZmFjaWxpdGF0b3IuIPCf"
        "kKM="
    ),
}


@lru_cache()
def _unwrap(key: str) -> str:
    return base64.b64decode(_VAULT[key]).decode("utf-8")


HINT_MESSAGE = _unwrap("hint")


def alternate_greeting(language: str) -> str | None:
    """A greeting the translation file has never heard of, if there is one."""
    return json.loads(_unwrap("greet")).get(language.upper())


def claim() -> str:
    """The 'you found it' banner, appended to the greeting."""
    return _unwrap("found")


def add_hint(response: HttpResponse) -> HttpResponse:
    """Nudge the curious toward the hunt without changing the body."""
    response[HINT_HEADER] = HINT_MESSAGE
    return response


def eggs(request: HttpRequest) -> HttpResponse:
    """Serves the riddle to anyone who asks."""
    return HttpResponse(
        _unwrap("riddle"),
        content_type="text/plain; charset=utf-8",
    )
