from django.http.response import JsonResponse, HttpResponse
from connexion_faker.base import FakerMockResolver

import random
import time


class DjangoFakerMockResolver(FakerMockResolver):
    def mock_operation(self, operation, *args, **kwargs):
        rand = random.random()

        if rand < self.internal_server_error_rate:
            return JsonResponse({"message": "Internal server error."}, status=500)

        status = self._get_success_response_status(operation.responses)
        response = operation.responses[status]

        if not "content" in response:
            return JsonResponse(None, status=int(status), safe=False)

        schema = response["content"]["application/json"]["schema"]
        resp = self._fake(schema)

        time.sleep(random.uniform(0, self.max_sleep))
        return JsonResponse(resp, safe=False)
