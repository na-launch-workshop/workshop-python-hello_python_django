import re

import pytest


@pytest.mark.django_db()
def test_returns_translation_with_timestamp(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/plain")

    text = response.content.decode()
    assert "hello world" in text.lower()
    assert re.search(r"@\s*\d{4}-\d{2}-\d{2}T", text)
