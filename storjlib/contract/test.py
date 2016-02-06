import os
import json
import unittest
import jsonschema
import pyjsonrpc


DEFAULT_RPC_URL = "http://127.0.0.1:7000"
STORJLIB_RPC_URL = os.environ.get("STORJLIB_RPC_URL", DEFAULT_RPC_URL)
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

    def test_missing_properties(self):
        keys = EXAMPLE_CONTRACT.keys()
        keys.remove("type")  # type must be set
        for key in keys:
            contract = EXAMPLE_CONTRACT.copy()
            del contract[key]
            self.assertFalse(self._is_valid(contract))

    @unittest.skip("not implemented")
    def test_invalid_renter_id(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_renter_address(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_renter_port(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_renter_signature(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_farmer_id(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_farmer_address(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_farmer_port(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_farmer_signature(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_data_size(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_data_hash(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_store_begin(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_store_duration(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_store_end(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_audit_algorithm(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_audit_count(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_audit_merkle_root(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_heartbeat_algorithm(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_heartbeat_count(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_heartbeat_coverage(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_currency(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_amount(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_download_price(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_destination(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_source(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_begin(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_settlements(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_interval(self):
        pass  # TODO implement


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
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)


@unittest.skip("not implemented")
class TestIsComplete(unittest.TestCase, _AbsTestIsValid):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)

    @unittest.skip("not implemented")
    def test_complete(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_missing_fields(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_signatures(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_store_timeframe(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_audit_algorithm(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_heatbeat_algorithm(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_heatbeat_coverage(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_currency(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_destination(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_invalid_payment_source(self):
        pass  # TODO implement


@unittest.skip("not implemented")
class TestSign(unittest.TestCase, _AbsTestIsValid):

    @unittest.skip("not implemented")
    def test_sign(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_sign_missing_non_signature_properties(self):
        pass  # TODO implement

    @unittest.skip("not implemented")
    def test_sign_already_signed(self):
        pass  # TODO implement


if __name__ == "__main__":
    unittest.main()
