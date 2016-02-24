import os
import unittest
import pyjsonrpc


# FIXME test entire swarm not just one node
DEFAULT_RPC_URL = "http://127.0.0.1:5001"
STORJNET_RPC_URL = os.environ.get("STORJNET_RPC_URL", DEFAULT_RPC_URL)


class TestDhtUserApi(unittest.TestCase):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJNET_RPC_URL)

    def test_id(self):
        self.assertIsNotNone(self.rpc.dht_id())

    def test_peers(self):
        peers = self.rpc.dht_peers()
        print("peers", peers)
        self.assertIsNotNone(peers)
        self.assertNotEqual(0, len(peers))

    def test_store(self):  # test put and get
        self.assertTrue(self.rpc.dht_put("testkey", "testvalue"))
        self.assertEqual(self.rpc.dht_get("testkey"), "testvalue")

    def test_find(self):
        nodeid = self.rpc.dht_id()
        result = self.rpc.dht_find(nodeid)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
