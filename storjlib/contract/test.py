import os
import binascii
import json
import unittest
import btctxstore
import jsonschema
import pyjsonrpc
from pycoin.encoding import a2b_hashed_base58


DEFAULT_RPC_URL = "http://127.0.0.1:7000"
STORJLIB_RPC_URL = os.environ.get("STORJLIB_RPC_URL", DEFAULT_RPC_URL)
CONTRACT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACT_SCHEMA_PATH = os.path.join(CONTRACT_DIR, "schema.json")
CONTRACT_SCHEMA = json.loads(open(CONTRACT_SCHEMA_PATH, 'r').read())
EXAMPLE_CONTRACT_PATH = os.path.join(CONTRACT_DIR, "example.json")
EXAMPLE_CONTRACT = json.loads(open(EXAMPLE_CONTRACT_PATH, 'r').read())


def btcaddress_to_hexnodeid(address):
    return binascii.hexlify(a2b_hashed_base58(address)[1:])


class _AbsContractTestIsValid(object):

    def test_example(self):
        self.assertTrue(self._validate(EXAMPLE_CONTRACT))

    def test_null_properties(self):
        keys = EXAMPLE_CONTRACT.keys()
        keys.remove("type")  # type must be set
        for key in keys:
            contract = EXAMPLE_CONTRACT.copy()
            contract[key] = None
            self.assertTrue(self._validate(contract))

    def test_extra_properties(self):
        contract = EXAMPLE_CONTRACT.copy()
        contract["extra"] = "test"
        self.assertFalse(self._validate(contract))

    def test_missing_properties(self):
        keys = EXAMPLE_CONTRACT.keys()
        keys.remove("type")  # type must be set
        for key in keys:
            contract = EXAMPLE_CONTRACT.copy()
            del contract[key]
            self.assertFalse(self._validate(contract))

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


class TestContractSpecSchema(unittest.TestCase, _AbsContractTestIsValid):
    """Test that the provided json schema from storjspec is correct."""

    def _validate(self, contract):
        try:
            jsonschema.validate(contract, CONTRACT_SCHEMA)
            return True
        except jsonschema.exceptions.ValidationError:
            return False


class TestContractValidate(unittest.TestCase, _AbsContractTestIsValid):
    """Test that the validate call from the rpc implementation is correct."""

    def _validate(self, contract):
        return self.rpc.contract_validate(contract)

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)


class TestContractIsComplete(unittest.TestCase):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)
        self.btctxstore = btctxstore.BtcTxStore()
        self.alice_key = self.btctxstore.create_wallet()
        self.bob_key = self.btctxstore.create_key()
        alice_wif = self.btctxstore.get_key(self.alice_key)
        alice_btcaddr = self.btctxstore.get_address(alice_wif)
        bob_btcaddr = self.btctxstore.get_address(self.bob_key)
        self.aliceid = btcaddress_to_hexnodeid(alice_btcaddr)
        self.bobid = btcaddress_to_hexnodeid(bob_btcaddr)

    def test_complete(self):
        contract = EXAMPLE_CONTRACT.copy()
        self.assertFalse(self.rpc.contract_is_complete(contract))
        contract["farmer_id"] = self.aliceid
        contract["renter_id"] = self.bobid
        self.assertFalse(self.rpc.contract_is_complete(contract))
        contract = self.rpc.contract_sign(contract, self.alice_key)
        contract = self.rpc.contract_sign(contract, self.bob_key)
        self.assertTrue(self.rpc.contract_is_complete(contract))

    def test_missing_fields(self):
        contract = EXAMPLE_CONTRACT.copy()
        contract["farmer_id"] = self.aliceid
        contract["renter_id"] = self.bobid
        contract = self.rpc.contract_sign(contract, self.alice_key)
        contract = self.rpc.contract_sign(contract, self.bob_key)
        self.assertTrue(self.rpc.contract_is_complete(contract))
        for key in contract.keys():
            _contract = contract.copy()
            _contract[key] = None
            self.assertFalse(self.rpc.contract_is_complete(_contract))

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


class TestContractSign(unittest.TestCase):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)
        self.btctxstore = btctxstore.BtcTxStore()
        self.alice_key = self.btctxstore.create_wallet()
        self.bob_key = self.btctxstore.create_key()
        alice_wif = self.btctxstore.get_key(self.alice_key)
        alice_btcaddr = self.btctxstore.get_address(alice_wif)
        bob_btcaddr = self.btctxstore.get_address(self.bob_key)
        self.aliceid = btcaddress_to_hexnodeid(alice_btcaddr)
        self.bobid = btcaddress_to_hexnodeid(bob_btcaddr)

    def test_sign(self):
        contract = EXAMPLE_CONTRACT.copy()
        contract["farmer_id"] = self.aliceid
        contract["renter_id"] = self.bobid
        contract = self.rpc.contract_sign(contract, self.alice_key)
        contract = self.rpc.contract_sign(contract, self.bob_key)
        self.assertTrue(self.rpc.contract_is_complete(contract))

    def test_sign_missing_non_signature_properties(self):
        def callback():
            contract = EXAMPLE_CONTRACT.copy()
            contract["farmer_id"] = self.aliceid
            self.rpc.contract_sign(contract, self.alice_key)
        self.assertRaises(pyjsonrpc.rpcerror.JsonRpcError, callback)

    def test_sign_already_signed(self):
        def callback():
            contract = EXAMPLE_CONTRACT.copy()
            contract["farmer_id"] = self.aliceid
            contract["renter_id"] = self.bobid
            contract = self.rpc.contract_sign(contract, self.alice_key)
            self.rpc.contract_sign(contract, self.alice_key)
        self.assertRaises(pyjsonrpc.rpcerror.JsonRpcError, callback)

    def test_invalid_key(self):
        def callback():
            contract = EXAMPLE_CONTRACT.copy()
            contract["farmer_id"] = self.aliceid
            contract["renter_id"] = self.bobid
            self.rpc.contract_sign(contract, "badkey")
        self.assertRaises(pyjsonrpc.rpcerror.JsonRpcError, callback)

    def test_incorrect_key(self):
        def callback():
            contract = EXAMPLE_CONTRACT.copy()
            contract["farmer_id"] = self.aliceid
            contract["renter_id"] = self.bobid
            self.rpc.contract_sign(contract, self.btctxstore.create_key())
        self.assertRaises(pyjsonrpc.rpcerror.JsonRpcError, callback)


if __name__ == "__main__":
    unittest.main()
