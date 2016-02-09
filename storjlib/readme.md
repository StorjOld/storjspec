# Storjlib specification and compatibility tests

[Python reference implementation](https://github.com/storj/storjlib)
[node.js reference implementation](https://github.com/Storj/node-storj)

 * [contract](contract): A storage contract defines obligations between farmer and renter.
 * [audit](audit): Provides proof of storage.
 * [heartbeat](heartbeat): Provides proof of availability. 


## User API Calls

| Command                | Arguments                                | Returns       | Description                                                   |
|------------------------|------------------------------------------|---------------|---------------------------------------------------------------|
| contract_validate      | contract                                 | bool          | Returns true if given object is a valid contract.             |
| contract_sign          | contract, key                            | contract      | Sign contract (all fields except signatures must be filled).  |
| contract_is_complete   | contract                                 | bool          | Returns true if given object is a complete signed contract.   |
|                        |                                          |               |                                                               |
| audit_prepare          | shardid, challenges                      | leaves        | Create the corresponding leaves for the given challenges.     |
| audit_perform          | shardid, leaves, challenge               | proof         | Proof format: [[node, [leaf, [response]]], node]              |
| audit_validate         | proof, root, challengenum, leaves        | bool          | Validate that the given proof is correct.                     |
|                        |                                          |               |                                                               |
| store_import           | paths                                    | shardid       | Import files/folders (behaves similar to zip).                |
| store_export           | shardid, path                            | paths         | Export a shard (behaves similar to unzip).                    |
| store_add              | path                                     | shardid       | Add an existing shard into the store.                         |
| store_remove           | shardid                                  |               | Remove a shard from the store.                                |


## Global hash function

All hashes are preformed with the following algorithm.

    ripemd160(sha256(data))

