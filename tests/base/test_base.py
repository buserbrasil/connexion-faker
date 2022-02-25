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
  result = faker_resolver._fake(_get_response_schema_from_path(faker_data, path))
  assert result == {"name": any_string(), "last_name": 'Andreas' }

def test_one_choice_route(faker_resolver, faker_data):
  path = '/one_choice'
  result = faker_resolver._fake(_get_response_schema_from_path(faker_data, path))
  assert result == { "name": any_string() }
  assert result["name"] in ['ok', '2']

def test_different_responses(faker_resolver, faker_data):
  path = '/different_responses'
  result = faker_resolver._get_success_response(_get_all_responses(faker_data, path))
  assert result == _get_all_responses(faker_data, path)["201"]

class any_string:
    def __eq__(self, other):
        return isinstance(other, str) and other

def _get_all_responses(faker_data, path):
  return faker_data['paths'][path]['get']['responses']

def _get_response_schema_from_path(faker_data, path):
  return _get_all_responses(faker_data, path)['200']['content']['application/json']['schema']
