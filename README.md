# Connexion Faker

[![PyPI](https://badge.fury.io/py/connexion-faker.svg)](https://pypi.org/project/connexion-faker/)

## Get Started

### Install

With poetry:
```sh
poetry add connexion-faker

# aiohttp
poetry add connexion-faker -E aiohttp

# django
poetry add connexion-faker -E django
```

With pip:
```sh
pip install connexion-faker
```

### Use

#### Setting OpenAPI file config

Add `x-fake` attribute in property key:

```yaml
openapi: "3.0.0"
info:
  title: Example
  version: 1.0.0
paths:
  /hello:
    get:
      summary: Hello
      responses:
        '200':
          description: Hello response.
          content:
            application/json:
              schema:
                type: object
                required:
                  - name
                properties:
                  name:
                    type: string
                    x-fake: name
```
- Can be YAML or JSON

#### AIOHTTP Resolver

```python
import connexion
from connexion_faker.aiohttp import AioHttpFakerMockResolver

resolver = AioHttpFakerMockResolver()

connexion_app = connexion.AioHttpApp(
    __name__, specification_dir="./", only_one_api=True
)
connexion_app.add_api(
    "./openapi.yml",
    validate_responses=True,
    pass_context_arg_name="request",
    resolver=resolver,
)
aiohttp_client(connexion_app.app)
```

#### Django Resolver

- Needs `django_connexion` lib [django-connexion](https://github.com/buserbrasil/django-connexion).

```python
from django_connexion import DjangoApi
from connexion_faker.django import DjangoFakerMockResolver
from django.urls import path

resolver = DjangoFakerMockResolver()
doc_api = DjangoApi("./tests/openapi.yml", resolver=resolver)

urlpatterns = [
    path('', doc_api.urls),
]
```

## Run tests

```
poetry run pytest
```
