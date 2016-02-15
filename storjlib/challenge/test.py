import os
import copy
import tempfile
import unittest
import hashlib
import pyjsonrpc
import binascii


DEFAULT_RPC_URL = "http://127.0.0.1:7000"
STORJLIB_RPC_URL = os.environ.get("STORJLIB_RPC_URL", DEFAULT_RPC_URL)


def h(hexdata):
    data = binascii.unhexlify(hexdata)
    digest = hashlib.new("ripemd160", hashlib.sha256(data).digest()).digest()
    return binascii.hexlify(digest)


def _c(n):
    seed = binascii.hexlify(os.urandom(32))
    return {"seed": seed, "offset": 0, "size": 0}


NUMCHALLENGES = 5
SHARD_DATA = os.urandom(1024)  # 1M
SHARD_HEXDATA = binascii.hexlify(SHARD_DATA)
SHARD_ID = h(SHARD_HEXDATA)
CHALLENGES = [_c(n) for n in range(NUMCHALLENGES)]
R0 = h(CHALLENGES[0]["seed"] + SHARD_HEXDATA)
R1 = h(CHALLENGES[1]["seed"] + SHARD_HEXDATA)
R2 = h(CHALLENGES[2]["seed"] + SHARD_HEXDATA)
R3 = h(CHALLENGES[3]["seed"] + SHARD_HEXDATA)
R4 = h(CHALLENGES[4]["seed"] + SHARD_HEXDATA)
R5 = ""
R6 = ""
R7 = ""
LEAVES = [h(R0), h(R1), h(R2), h(R3), h(R4)]
ALL_LEAVES = [h(R0), h(R1), h(R2), h(R3), h(R4), h(R5), h(R6), h(R7)]
L0, L1, L2, L3, L4, L5, L6, L7 = ALL_LEAVES
ROOT = h(h(h(L0 + L1) + h(L2 + L3)) + h(h(L4 + L5) + h(L6 + L7)))
AUDIT_CHALLENGE = CHALLENGES[3]
HEARTBEAT_CHALLENGE = CHALLENGES[4]
N01 = h(L0 + L1)
N4567 = h(h(L4 + L5) + h(L6 + L7))
PROOF = [[N01, [L2, [R3]]], N4567]


class _AbsAudit(object):

    def setUp(self):
        self.rpc = pyjsonrpc.HttpClient(url=STORJLIB_RPC_URL)

        # save temp shard
        shard_path = tempfile.mktemp()
        with open(shard_path, "wb") as shard:
            shard.write(SHARD_DATA)

        self.shardid = self.rpc.store_add(shard_path)  # import shard
        os.remove(shard_path)  # remove temp shard

    def tearDown(self):
        self.rpc.store_remove(self.shardid)  # remove temp shard from store


class TestAuditPrepare(_AbsAudit, unittest.TestCase):

    def test_prepare(self):
        self.assertEqual(self.shardid, SHARD_ID)
        leaves = self.rpc.challenge_prepare(SHARD_ID, CHALLENGES)
        self.assertEqual(leaves, LEAVES)


class TestAuditPerform(_AbsAudit, unittest.TestCase):

    def test_preform(self):
        self.assertEqual(self.shardid, SHARD_ID)
        proof = self.rpc.challenge_perform(SHARD_ID, LEAVES, AUDIT_CHALLENGE)
        self.assertEqual(proof, PROOF)

    # TODO test size and offset
    # TODO test invalid input


class TestAuditValidate(_AbsAudit, unittest.TestCase):

    def test_validate(self):
        self.assertTrue(self.rpc.challenge_validate(PROOF, ROOT, 3, LEAVES))

    def test_invalid_challange_response(self):
        # attacker provides proof with the wrong response hoping its not checked
        # does not match any leaf
        proof = copy.deepcopy(PROOF)
        proof[0][1][1] = h("DEADBEEF")
        self.assertFalse(self.rpc.challenge_validate(proof, ROOT, 3, LEAVES))

    def test_proof_to_shallow(self):
        # attacker provides a shallow proof hoping the depth is not checked
        self.assertFalse(self.rpc.challenge_validate(PROOF, ROOT, 4, LEAVES))

    def test_proof_for_wrong_leaf(self):
        # attacker provides proof for an old challenge hoping its not checked
        # match wrong leaf
        proof = self.rpc.challenge_perform(SHARD_ID, LEAVES, CHALLENGES[2])
        self.assertFalse(self.rpc.challenge_validate(proof, ROOT, 3, LEAVES))

    def test_proof_for_wrong_root(self):
        # attacker provides proof for wrong merkle root hoping its not checked
        root = h("DEADBEEF")
        self.assertFalse(self.rpc.challenge_validate(PROOF, root, 3, LEAVES))

    # TODO other possible invalid proofs?
    # TODO test invalid input formats


if __name__ == "__main__":
    unittest.main()
