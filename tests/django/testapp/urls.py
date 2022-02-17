from django_connexion import DjangoApi
from connexion_faker.django import DjangoFakerMockResolver
from django.urls import path

resolver = DjangoFakerMockResolver()
doc_api = DjangoApi("./tests/openapi.yml", resolver=resolver)

urlpatterns = [
    path('', doc_api.urls),
]
