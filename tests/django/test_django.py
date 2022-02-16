import pytest
from django_connexion.tests.testapp import views
from django_connexion import DjangoApi
from connexion_faker.django import DjangoFakerMockResolver

# @pytest.fixture
# def cli(loop, client):
#     resolver = DjangoFakerMockResolver()

#     doc_api = DjangoApi("./tests/openapi.yml", resolver=resolver)
#     print(client)

#     return loop.run_until_complete(client)


def test_hello_name(rf):
    # print(rf.__dict__)
    request = rf.get("/hello")
    resp = request
    resolver = DjangoFakerMockResolver()
    doc_api = DjangoApi("./tests/openapi.yml", resolver=resolver)
    print(doc_api)
    print(doc_api.__dict__)
    # assert resp.status == 200
    assert resp.json() == {"name": any_string()}


class any_string:
    def __eq__(self, other):
        return isinstance(other, str) and other
