import os
import time
import binascii
import random
import unittest
import pyjsonrpc


SWARMSIZE = int(os.environ.get("STORJNET_SWARMSIZE", "50"))
USER_HOST = os.environ.get("STORJNET_USER_HOST", "127.0.0.1")
USER_START_PORT = int(os.environ.get("STORJNET_USER_START_PORT", "5000"))


# FIXME test if input is sanitized


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
        self.assertEqual(len(result), 2)
        ip, port = result
        self.assertIsInstance(ip, unicode)
        self.assertIsInstance(port, int)
        # TODO check if valid ip

    def test_find_peer(self):
        node = random.choice(self.swarm)
        hexnodeid = node.dht_id()
        peer = node.dht_peers()
        peerid, peerip, peer_port = random.choice(peer)
        self.assertNotEqual(peerid, hexnodeid)
        found_ip, found_port = node.dht_find(peerid)
        self.assertEqual(peerip, found_ip)
        self.assertEqual(peer_port, found_port)

    def test_find_offline(self):
        node = random.choice(self.swarm)
        hexnodeid = binascii.hexlify(os.urandom(20))
        result = node.dht_find(hexnodeid)
        self.assertIsNone(result)

    def test_stun(self):
        node = random.choice(self.swarm)
        result = node.dht_stun()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        ip, port = result
        self.assertIsInstance(ip, unicode)
        self.assertIsInstance(port, int)
        # TODO check if valid ip


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
            message = binascii.hexlify(os.urandom(64))

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

            # check queue empty after call to message_list
            self.assertFalse(bool(receiver.message_list()))

    def test_ordering(self):
        sender = self.swarm[0]
        receiver = self.swarm[-1]

        # send messages
        message_alpha = binascii.hexlify(os.urandom(64))
        message_beta = binascii.hexlify(os.urandom(64))
        message_gamma = binascii.hexlify(os.urandom(64))
        self.assertTrue(sender.message_send(receiver.dht_id(), message_alpha))
        self.assertTrue(sender.message_send(receiver.dht_id(), message_beta))
        self.assertTrue(sender.message_send(receiver.dht_id(), message_gamma))

        # check received in order
        received = receiver.message_list()
        self.assertTrue(sender.dht_id() in received)
        messages = received[sender.dht_id()]
        self.assertEqual(messages[0], message_alpha)
        self.assertEqual(messages[1], message_beta)
        self.assertEqual(messages[2], message_gamma)

    def test_send_to_self(self):
        sender = random.choice(self.swarm)
        receiver = sender
        message = binascii.hexlify(os.urandom(64))

        # send message
        self.assertTrue(sender.message_send(receiver.dht_id(), message))

        # check received
        received = receiver.message_list()
        self.assertTrue(sender.dht_id() in received)
        messages = received[sender.dht_id()]
        self.assertTrue(len(messages) == 1)
        self.assertEqual(messages[0], message)

    def test_json(self):
        sender = self.swarm[0]
        receiver = self.swarm[-1]
        message = {
            "test_object": {"foo": "bar"},
            "test_array": [0, 1, 2, 3, 4, 5],
            "test_integer": 42,
            "test_float": 3.14,
            "test_bool": True,
            "test_null": None,
        }

        # send message
        self.assertTrue(sender.message_send(receiver.dht_id(), message))

        # check received
        received = receiver.message_list()
        self.assertTrue(sender.dht_id() in received)
        messages = received[sender.dht_id()]
        self.assertTrue(len(messages) == 1)
        self.assertEqual(messages[0], message)

    def test_send_to_void(self):
        sender = random.choice(self.swarm)
        message = binascii.hexlify(os.urandom(64))
        receiverid = binascii.hexlify(os.urandom(20))
        self.assertFalse(sender.message_send(receiverid, message))

    def test_queue_full(self):
        pass


class TestPubSubUserApi(unittest.TestCase):

    def setUp(self):
        self.swarm = []
        for i in range(SWARMSIZE):
            url = "http://{0}:{1}".format(USER_HOST, USER_START_PORT + i)
            self.swarm.append(pyjsonrpc.HttpClient(url=url))

    # TODO test json event
    # TODO history checked
    # TODO test queue full

    def test_subscriptions(self):
        peer = random.choice(self.swarm)
        self.assertNotIn("test_subscriptions", peer.pubsub_subscriptions())
        peer.pubsub_subscribe("test_subscriptions")
        self.assertIn("test_subscriptions", peer.pubsub_subscriptions())
        peer.pubsub_unsubscribe("test_subscriptions")
        self.assertNotIn("test_subscriptions", peer.pubsub_subscriptions())

    def test_flood(self):
        # every node subscribes and should receive  the event
        topic = "test_flood_{0}".format(binascii.hexlify(os.urandom(32)))

        for peer in self.swarm:
            peer.pubsub_subscribe(topic)

        # wait until subscriptions propagate
        time.sleep(5)

        # send event
        peer = random.choice(self.swarm)
        event = binascii.hexlify(os.urandom(32))
        peer.pubsub_publish(topic, event)

        # wait until event propagates
        time.sleep(5)

        # check all peers received the event
        for peer in self.swarm:
            events = peer.pubsub_events(topic)
            self.assertEqual(events, [event])

    def test_multihop(self):
        topic = "test_miltihop_{0}".format(binascii.hexlify(os.urandom(32)))
        sender = self.swarm[0]
        receiver = self.swarm[-1]
        receiver.pubsub_subscribe(topic)

        # wait until subscriptions propagate
        time.sleep(5)

        # send event
        event = binascii.hexlify(os.urandom(32))
        sender.pubsub_publish(topic, event)

        # wait until event propagates
        time.sleep(5)

        # check all peers received the event
        events = receiver.pubsub_events(topic)
        self.assertEqual(events, [event])


if __name__ == "__main__":
    unittest.main()
