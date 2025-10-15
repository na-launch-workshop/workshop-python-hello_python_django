#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "translation_service.settings")

    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        has_addr = any(not arg.startswith("-") for arg in sys.argv[2:])
        if not has_addr:
            from app.config import load_config

            cfg = load_config()
            sys.argv.append(f"0.0.0.0:{cfg.port}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover - stub until Django installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PATH?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
