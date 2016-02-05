import os
import json
import unittest
import jsonschema
import pyjsonrpc


DEFAULT_RPC_URL = "http://127.0.0.1:7000"
STORJTERMS_RPC_URL = os.environ.get("STORJTERMS_RPC_URL", DEFAULT_RPC_URL)
CONTRACT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACT_SCHEMA_PATH = os.path.join(CONTRACT_DIR, "schema.json")
CONTRACT_SCHEMA = json.loads(open(CONTRACT_SCHEMA_PATH, 'r').read())
EXAMPLE_CONTRACT_PATH = os.path.join(CONTRACT_DIR, "example.json")
EXAMPLE_CONTRACT = json.loads(open(EXAMPLE_CONTRACT_PATH, 'r').read())


class _AbsTestIsValid(object):

    def test_example(self):
        self.assertTrue(self._is_valid(EXAMPLE_CONTRACT))

    def test_null_properties(self):
        keys = EXAMPLE_CONTRACT.keys()
        keys.remove("type")  # type must be set
        for key in keys:
            contract = EXAMPLE_CONTRACT.copy()
            contract[key] = None
            self.assertTrue(self._is_valid(contract))

    def test_extra_properties(self):
        contract = EXAMPLE_CONTRACT.copy()
        contract["extra"] = "test"
        self.assertFalse(self._is_valid(contract))

    # TODO test missing properties
    # TODO test invalid properties


class TestIsValidSpec(unittest.TestCase, _AbsTestIsValid):
    """Test that the provided json schema from storjspec is correct."""

    def _is_valid(self, contract):
        try:
            jsonschema.validate(contract, CONTRACT_SCHEMA)
            return True
        except jsonschema.exceptions.ValidationError:
            return False


class TestIsValid(unittest.TestCase, _AbsTestIsValid):
    """Test that the is_valid call from the rpc implementation is correct."""

    def _is_valid(self, contract):
        return self.rpc.contract_is_valid(contract)

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJTERMS_RPC_URL)


# TODO test is_valid
# TODO test sign
# TODO test is_complete


if __name__ == "__main__":
    unittest.main()
