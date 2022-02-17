import pytest
import connexion
from connexion_faker.aiohttp import AioHttpFakerMockResolver


@pytest.fixture
def cli(loop, aiohttp_client):
    resolver = AioHttpFakerMockResolver()

    connexion_app = connexion.AioHttpApp(
        __name__, specification_dir="../../", only_one_api=True
    )
    connexion_app.add_api(
        "./tests/openapi.yml",
        validate_responses=True,
        pass_context_arg_name="request",
        resolver=resolver,
    )

    return loop.run_until_complete(aiohttp_client(connexion_app.app))


async def test_hello_name(cli):
    resp = await cli.get("/hello")
    assert resp.status == 200
    assert await resp.json() == {"name": any_string()}


class any_string:
    def __eq__(self, other):
        return isinstance(other, str) and other
