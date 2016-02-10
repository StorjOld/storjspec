# Storage audit and heartbeats

The farmer provides proof of storage by hashing a given challenge with the
shard data. The correctness of the audit/heartbeat response can be verified via
a Merkle tree, which is given by the renter on shard transfer and the root
stored in the contract. 


## Generating audit/heartbeat challenges

TODO describe


## Generating the Merkle tree

TODO describe


## Preforming the audit/heartbeat response

TODO describe


## Verification of the audit/heartbeat with the Merkle tree

TODO describe


Merkle leaf = hash(hash(challenge + data))
Padded leaf = hash("")

![scheme](scheme.png)
