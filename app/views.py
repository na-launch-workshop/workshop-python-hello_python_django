from __future__ import annotations

import json
from datetime import timezone
from functools import lru_cache

from django.http import HttpRequest, HttpResponse
from django.utils import timezone as django_timezone

from . import easter_eggs
from .config import AppConfig, load_config

ERROR_INVALID_JSON = "Invalid JSON format in {filename}"
ERROR_MISSING_FILE = "Could not find {filename} in resources."


@lru_cache()
def _config() -> AppConfig:
    return load_config()


def read_root(request: HttpRequest) -> HttpResponse:
    cfg = _config()

    try:
        payload = cfg.translation_file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return HttpResponse(
            ERROR_MISSING_FILE.format(filename=cfg.translation_file_name),
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return HttpResponse(
            ERROR_INVALID_JSON.format(filename=cfg.translation_file_name),
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    translations = data.get("translations") if isinstance(data, dict) else None
    if not isinstance(translations, dict):
        return HttpResponse(
            ERROR_INVALID_JSON.format(filename=cfg.translation_file_name),
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    secret = easter_eggs.alternate_greeting(cfg.default_language)
    translation = secret or translations.get(cfg.default_language) or translations.get("EN")
    if not isinstance(translation, str):
        return HttpResponse(
            ERROR_INVALID_JSON.format(filename=cfg.translation_file_name),
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    timestamp = django_timezone.now().astimezone(timezone.utc).isoformat()
    body = f"{translation} @ {timestamp}"
    if secret:
        body += easter_eggs.claim()

    return easter_eggs.add_hint(
        HttpResponse(
            body,
            content_type="text/plain; charset=utf-8",
        )
    )
