from connexion_faker.base import FakerMockResolver
import pytest
import yaml

@pytest.fixture
def faker_resolver():
    return FakerMockResolver()

@pytest.fixture
def faker_data():
  with open("./tests/openapi.yml") as f:
    data = yaml.load(f, Loader=yaml.Loader)
  return data

def test_hello_route(faker_resolver, faker_data):
  path = '/hello'
  schema = _get_response_schema_from_path(faker_data, path, '200')
  result = faker_resolver._fake(schema)
  assert result == {"name": any_string(), "last_name": 'Andreas' }

def test_one_choice_route(faker_resolver, faker_data):
  path = '/one_choice'
  schema = _get_response_schema_from_path(faker_data, path, '200')
  result = faker_resolver._fake(schema)
  assert result == { "name": any_string() }
  assert result["name"] in ['ok', '2']

def test_different_responses(faker_resolver, faker_data):
  path = '/different_responses'
  all_responses = _get_all_responses(faker_data, path)

  status = faker_resolver._get_success_response_status(all_responses)
  assert all_responses[status] == all_responses["201"]

def test_different_responses(faker_resolver, faker_data):
  path = '/different_responses_2'
  all_responses = _get_all_responses(faker_data, path)

  status = faker_resolver._get_success_response_status(all_responses)
  assert status == '204'

class any_string:
    def __eq__(self, other):
        return isinstance(other, str) and other

def _get_all_responses(faker_data, path):
  return faker_data['paths'][path]['get']['responses']

def _get_response_schema_from_path(faker_data, path, status):
  response = _get_all_responses(faker_data, path)[status]
  if 'content' in response:
    return response['content']['application/json']['schema']
  return None
