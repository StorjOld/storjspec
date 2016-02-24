import os
import random
import unittest
import pyjsonrpc


# FIXME add to readme documentation
SWARMSIZE = int(os.environ.get("STORJNET_SWARMSIZE", "50"))
USER_HOST = os.environ.get("STORJNET_USER_HOST", "127.0.0.1")
USER_START_PORT = int(os.environ.get("STORJNET_USER_START_PORT", "5000"))


class TestDhtUserApi(unittest.TestCase):

    def setUp(self):
        self.swarm = []
        for i in range(SWARMSIZE):
            url = "http://{0}:{1}".format(USER_HOST, USER_START_PORT + i)
            self.swarm.append(pyjsonrpc.HttpClient(url=url))

    def test_id(self):
        node = random.choice(self.swarm)
        self.assertIsNotNone(node.dht_id())

    def test_peers(self):
        node = random.choice(self.swarm)
        peers = node.dht_peers()
        self.assertIsNotNone(peers)
        self.assertNotEqual(0, len(peers))

    def test_store(self):  # test put and get
        # randomly store and retrieve 20 key/value pairs
        for i in range(20):
            put_node = random.choice(self.swarm)
            get_node = random.choice(self.swarm)
            test_key = "test_key_{0}".format(i)
            test_value = "test_value_{0}".format(i)
            self.assertTrue(put_node.dht_put(test_key, test_value))
            self.assertEqual(get_node.dht_get(test_key), test_value)

    def test_find_self(self):
        node = random.choice(self.swarm)
        nodeid = node.dht_id()
        result = node.dht_find(nodeid)
        self.assertIsNotNone(result)

    def test_find_peer(self):
        node = random.choice(self.swarm)
        nodeid = node.dht_id()
        peer = node.dht_peers()
        peerid, peerip, peer_port = random.choice(peer)
        self.assertNotEqual(peerid, nodeid)
        found_ip, found_port = node.dht_find(peerid)
        self.assertEqual(peerip, found_ip)
        self.assertEqual(peer_port, found_port)


if __name__ == "__main__":
    unittest.main()
