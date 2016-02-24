import os
import unittest
import pyjsonrpc


# FIXME require more then 1 rpc url to test swarm
DEFAULT_RPC_URL = "http://127.0.0.1:5000"
STORJNET_RPC_URL = os.environ.get("STORJNET_RPC_URL", DEFAULT_RPC_URL)


class TestDhtUserApi(unittest.TestCase):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJNET_RPC_URL)

    def test_store(self):
        self.assertTrue(self.rpc.dht_put("testkey", "testvalue"))
        self.assertEqual(self.rpc.dht_get("testkey"), "testvalue")

    def test_find(self):
        nodeid = self.rpc.dht_id()
        result = self.rpc.dht_find(nodeid)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
