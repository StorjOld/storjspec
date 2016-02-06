import os
import unittest
import hashlib
import pyjsonrpc


DEFAULT_RPC_URL = "http://127.0.0.1:7000"
STORJLIB_RPC_URL = os.environ.get("STORJLIB_RPC_URL", DEFAULT_RPC_URL)


def h(data):
    return hashlib.new("ripemd160", hashlib.sha256(data).digest()).digest()


NUMCHALLENGES = 5
SHARDDATA = b"monkey butt"
CHALLANGES = [os.urandom(32) for n in range(NUMCHALLENGES)]
R0 = h(CHALLANGES[0] + SHARDDATA)
R1 = h(CHALLANGES[1] + SHARDDATA)
R2 = h(CHALLANGES[2] + SHARDDATA)
R3 = h(CHALLANGES[3] + SHARDDATA)
R4 = h(CHALLANGES[4] + SHARDDATA)
R5 = h("" + SHARDDATA)
R6 = h("" + SHARDDATA)
R7 = h("" + SHARDDATA)
L0, L1, L2, L3, L4, L5, L6, L7 = (h(R0), h(R1), h(R2), h(R3),
                                  h(R4), h(R5), h(R6), h(R7))
ROOT = h(h(h(L0 + L1) + h(L2 + L3)) + h(h(L4 + L5) + h(L6 + L7)))
CHALLENGE = CHALLANGES[3]
N01 = h(L0 + L1)
N4567 = h(h(L4 + L5) + h(L6 + L7))
PROOF = [N01, [L2, [R3]], N4567]


@unittest.skip("not implemented")
class TestPrepare(unittest.TestCase):
    pass


@unittest.skip("not implemented")
class TestPerform(unittest.TestCase):
    pass


@unittest.skip("not implemented")
class TestValidate(unittest.TestCase):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)

    def test_validate(self):
        self.assertTrue(self.rpc.audit_validate(PROOF, ROOT, CHALLENGE,
                                                NUMCHALLENGES))

    # TODO test invalid proofs


@unittest.skip("not implemented")
class TestPerform(unittest.TestCase):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)

    # TODO test audit_perform
    # TODO test audit_prepare


if __name__ == "__main__":
    unittest.main()
