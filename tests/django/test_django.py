import pytest

def test_settings(settings):
    assert settings.ROOT_URLCONF == "tests.django.testapp.urls"
    assert settings.INSTALLED_APPS == ['tests.django.testapp']

def test_hello_name(client):
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.json() == {"name": any_string()}

def test_wrong_path(client):
    resp = client.get("/dark")
    assert resp.status_code == 404
    assert 'Not Found' in resp.content.decode("utf-8")

class any_string:
    def __eq__(self, other):
        return isinstance(other, str) and other
