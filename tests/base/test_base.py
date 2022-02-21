from connexion_faker.base import FakerMockResolver
import pytest
import yaml

@pytest.fixture
def faker_resolver():
    return FakerMockResolver()

@pytest.fixture
def faker_data():
  with open("./tests/base/swagger.yaml") as f:
    data = yaml.load(f, Loader=yaml.Loader)
  return data

def test_hello_route(faker_resolver, faker_data):
  path = '/hello'
  result = faker_resolver._fake(get_response_schema_from_path(faker_data, path))
  assert result == {"name": any_string(), "last_name": 'Andreas' }

def test_one_choice_route(faker_resolver, faker_data):
  path = '/one_choice'
  result = faker_resolver._fake(get_response_schema_from_path(faker_data, path))
  assert result == { "name": any_string() }
  assert result["name"] in ['ok', 2]

class any_string:
    def __eq__(self, other):
        return isinstance(other, str) and other

def get_response_schema_from_path(faker_data, path):
  return faker_data['paths'][path]['get']['responses']['200']['content']['application/json']['schema']
