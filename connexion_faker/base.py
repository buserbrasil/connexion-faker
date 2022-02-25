import string
import importlib
import random
from connexion.mock import MockResolver
from faker import Faker


class FakerMockResolver(MockResolver):
    def __init__(self, internal_server_error_rate=0.0, max_sleep=1.5, locale=None):
        super().__init__(True)
        self.faker = Faker(locale)
        self.internal_server_error_rate = internal_server_error_rate
        self.max_sleep = max_sleep

    def _get_success_response_status(self, responses):
        success_respons_statuses = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
        for response_status in success_respons_statuses:
            if str(response_status) in responses:
                return str(response_status)

    def _fake(self, schema):
        if "x-fake" in schema:
            if schema["x-fake"] == 'example':
                return schema["example"]

            if schema["x-fake"].startswith("?") or schema["x-fake"].startswith("#"):
                parts = schema["x-fake"].split(" ")
                letters = string.ascii_letters
                text = parts[0]
                if len(parts) > 1:
                    letters = "".join(parts[1:]).strip()
                return self.faker.bothify(text, letters)

            if schema["x-fake"].startswith("fn:"):
                module_name, fn_name = schema["x-fake"][len("fn:") :].split(":", 1)
                module = importlib.import_module(module_name)
                return getattr(module, fn_name)()

            return getattr(self.faker, schema["x-fake"])()

        if "enum" in schema:
            return random.choice(schema["enum"])

        if "oneOf" in schema:
            component = random.choice(schema["oneOf"])
            return self._fake(component)

        if schema["type"].lower() == "array":
            return [
                self._fake(schema["items"])
                for _ in range(
                    random.randint(
                        schema.get("minItems", 3), schema.get("maxItems", 10)
                    )
                )
            ]

        if schema["type"].lower() == "object":
            return {k: self._fake(v) for k, v in schema["properties"].items()}

        if schema["type"].lower() == "string":
            format = schema.get("format", "word")

            return getattr(self.faker, format.replace("-", "_"))()

        if schema["type"].lower().startswith("int") or schema["type"] == "number":
            return self.faker.random_int()

        return getattr(self.faker, schema.get("type", "word"))()
