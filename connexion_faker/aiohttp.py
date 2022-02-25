import random
import time

from aiohttp import web
from connexion_faker.base import FakerMockResolver


class AioHttpFakerMockResolver(FakerMockResolver):
    def mock_operation(self, operation, *args, **kwargs):
        rand = random.random()

        if rand < self.internal_server_error_rate:
            return web.json_response({"message": "Internal server error."}, status=500)

        response = self._get_success_response(operation.responses)
        print(operation.responses)
        print(response)
        print(response["content"])
        schema = response["content"]["application/json"]["schema"]
        resp = self._fake(schema), 200

        time.sleep(random.uniform(0, self.max_sleep))
        return resp
