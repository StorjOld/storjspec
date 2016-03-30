import os
import time
import binascii
import random
import unittest
import pyjsonrpc


SWARMSIZE = int(os.environ.get("STORJNET_SWARMSIZE", "50"))
USER_HOST = os.environ.get("STORJNET_USER_HOST", "127.0.0.1")
USER_START_PORT = int(os.environ.get("STORJNET_USER_START_PORT", "5000"))


SLEEP_TIME = 4


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
        random.shuffle(self.swarm)
        senders = self.swarm[:len(self.swarm)/2]
        receivers = self.swarm[len(self.swarm)/2:]
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
        random.shuffle(self.swarm)
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
        random.shuffle(self.swarm)
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
        time.sleep(SLEEP_TIME)

        # send event
        peer = random.choice(self.swarm)
        event = binascii.hexlify(os.urandom(32))
        peer.pubsub_publish(topic, event)

        # wait until event propagates
        time.sleep(SLEEP_TIME)

        # check all peers received the event
        for peer in self.swarm:
            events = peer.pubsub_events(topic)
            self.assertEqual(events, [event])

    def test_multihop(self):
        random.shuffle(self.swarm)
        senders = self.swarm[:len(self.swarm)]
        receivers = self.swarm[len(self.swarm):]
        for sender, receiver in zip(senders, receivers):

            # receiver subscribes to topic
            topic = "test_miltihop_{0}".format(binascii.hexlify(os.urandom(32)))
            receiver.pubsub_subscribe(topic)

            # wait until subscriptions propagate
            time.sleep(SLEEP_TIME)

            # send event
            event = binascii.hexlify(os.urandom(32))
            sender.pubsub_publish(topic, event)

            # wait until event propagates
            time.sleep(SLEEP_TIME)

            # check all peers received the event
            events = receiver.pubsub_events(topic)
            self.assertEqual(events, [event])


class TestStreamUserApi(unittest.TestCase):

    def setUp(self):
        self.swarm = []
        for i in range(SWARMSIZE):
            url = "http://{0}:{1}".format(USER_HOST, USER_START_PORT + i)
            self.swarm.append(pyjsonrpc.HttpClient(url=url))

    def test_open(self):
        random.shuffle(self.swarm)
        alice = self.swarm[0]
        bob = self.swarm[-1]
        streamid = alice.stream_open(bob.dht_id())
        self.assertIsNotNone(streamid)

    # TODO test both can open

    def test_io(self):
        random.shuffle(self.swarm)
        alice = self.swarm[0]
        bob = self.swarm[1]

        # open stream
        hexstreamid = alice.stream_open(bob.dht_id())
        self.assertIsNotNone(hexstreamid)

        # write alice to bob
        alice_hexdata = binascii.hexlify(os.urandom(32))
        bytes_written = alice.stream_write(hexstreamid, alice_hexdata)
        self.assertEqual(bytes_written, 32)

        # write bob to alice
        bob_hexdata = binascii.hexlify(os.urandom(32))
        bytes_written = bob.stream_write(hexstreamid, bob_hexdata)
        self.assertEqual(bytes_written, 32)

        # read alice from bob
        read_data = alice.stream_read(hexstreamid)
        self.assertEqual(read_data, bob_hexdata)

        # read bob from alice
        read_data = bob.stream_read(hexstreamid)
        self.assertEqual(read_data, alice_hexdata)

    def test_close(self):
        random.shuffle(self.swarm)
        alice = self.swarm[0]
        bob = self.swarm[1]

        # open stream
        hexstreamid = alice.stream_open(bob.dht_id())
        self.assertIsNotNone(hexstreamid)

        # transfer works before
        written_hexdata = binascii.hexlify(os.urandom(32))
        bytes_written = alice.stream_write(hexstreamid, written_hexdata)
        self.assertEqual(bytes_written, 32)
        read_hexdata = bob.stream_read(hexstreamid)
        self.assertEqual(read_hexdata, written_hexdata)

        # test close
        self.assertTrue(alice.stream_close(hexstreamid))

        # write fails on closed stream
        written_hexdata = binascii.hexlify(os.urandom(32))
        bytes_written = alice.stream_write(hexstreamid, written_hexdata)
        self.assertEqual(bytes_written, None)

        # read fails on closed stream
        read_hexdata = bob.stream_read(hexstreamid)
        self.assertEqual(read_hexdata, None)

    # TODO test both can close

    def test_list(self):

        random.shuffle(self.swarm)
        alice = self.swarm[0]
        bob = self.swarm[1]
        charlie = self.swarm[2]

        # alice -> bob
        alpha_hexstreamid = alice.stream_open(bob.dht_id())
        self.assertIsNotNone(alpha_hexstreamid)

        # alice -> bob
        beta_hexstreamid = alice.stream_open(bob.dht_id())
        self.assertIsNotNone(beta_hexstreamid)

        # charlie -> alice
        gamma_hexstreamid = charlie.stream_open(alice.dht_id())
        self.assertIsNotNone(gamma_hexstreamid)

        alice_streams = alice.stream_list()
        self.assertEqual(len(alice_streams), 3)
        self.assertIn(alpha_hexstreamid, alice_streams)
        self.assertEqual(alice_streams[alpha_hexstreamid][0], bob.dht_id())
        self.assertIn(beta_hexstreamid, alice_streams)
        self.assertEqual(alice_streams[beta_hexstreamid][0], bob.dht_id())
        self.assertIn(gamma_hexstreamid, alice_streams)
        self.assertEqual(alice_streams[gamma_hexstreamid][0], charlie.dht_id())

        bob_streams = bob.stream_list()
        self.assertEqual(len(bob_streams), 2)
        self.assertIn(alpha_hexstreamid, bob_streams)
        self.assertEqual(bob_streams[alpha_hexstreamid][0], alice.dht_id())
        self.assertIn(beta_hexstreamid, bob_streams)
        self.assertEqual(bob_streams[beta_hexstreamid][0], alice.dht_id())

        charlie_streams = charlie.stream_list()
        self.assertEqual(len(charlie_streams), 1)
        self.assertIn(gamma_hexstreamid, charlie_streams)
        self.assertEqual(charlie_streams[gamma_hexstreamid][0], alice.dht_id())


class TestStreamUserApiErrors(unittest.TestCase):

    def setUp(self):
        self.swarm = []
        for i in range(SWARMSIZE):
            url = "http://{0}:{1}".format(USER_HOST, USER_START_PORT + i)
            self.swarm.append(pyjsonrpc.HttpClient(url=url))

    def test_wrong_streamid(self):
        random.shuffle(self.swarm)
        alice = self.swarm[0]

        hexdata = binascii.hexlify(os.urandom(32))
        wrongstreamid = binascii.hexlify(os.urandom(32))

        # write wrong streamid
        bytes_written = alice.stream_write(wrongstreamid, hexdata)
        self.assertEqual(bytes_written, None)

        # close wrong streamid
        self.assertFalse(alice.stream_close(wrongstreamid))


if __name__ == "__main__":
    unittest.main()
