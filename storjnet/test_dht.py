import os
import binascii
import random
import unittest
import pyjsonrpc


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
        hexnodeid = node.dht_id()
        result = node.dht_find(hexnodeid)
        self.assertIsNotNone(result)

    def test_find_peer(self):
        node = random.choice(self.swarm)
        hexnodeid = node.dht_id()
        peer = node.dht_peers()
        peerid, peerip, peer_port = random.choice(peer)
        self.assertNotEqual(peerid, hexnodeid)
        found_ip, found_port = node.dht_find(peerid)
        self.assertEqual(peerip, found_ip)
        self.assertEqual(peer_port, found_port)

    # TODO test find offline
    # TODO test stun


class TestMessageUserApi(unittest.TestCase):

    def setUp(self):
        self.swarm = []
        for i in range(SWARMSIZE):
            url = "http://{0}:{1}".format(USER_HOST, USER_START_PORT + i)
            self.swarm.append(pyjsonrpc.HttpClient(url=url))

    def test_send_receive(self):
        senders = self.swarm[:len(self.swarm)/2]
        receivers = self.swarm[len(self.swarm)/2:]
        random.shuffle(senders)
        random.shuffle(receivers)
        for sender, receiver in zip(senders, receivers):
            message = binascii.hexlify(os.urandom(32))

            # check queue previously empty
            self.assertFalse(bool(receiver.message_list()))

            # send message
            self.assertTrue(sender.message_send(receiver.dht_id(), message))

            # check received
            received = receiver.message_list()
            self.assertTrue(sender.dht_id() in received)
            messages = received[sender.dht_id()]
            self.assertTrue(len(messages) == 1)
            self.assertEqual(messages[0], message)

    def test_ordering(self):
        pass

    def test_json(self):
        pass

    def test_send_to_void(self):
        pass


if __name__ == "__main__":
    unittest.main()
