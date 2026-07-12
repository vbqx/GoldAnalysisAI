from src.data.url_redact import redact_url


def test_redact_url_strips_credentials() -> None:
    assert redact_url("http://user:secret@proxy.example.com:8080/path") == "http://proxy.example.com:8080"
