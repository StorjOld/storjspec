# Storjlib specification and compatibility tests

Components

 * [contract](contract): A storage contract defines obligations between farmer and renter.
 * [challenge](challenge): Audits provide proof of storage and heartbeats proof of availability.


Reference implementations

 * [Python](https://github.com/storj/storjlib)
 * [node.js](https://github.com/Storj/node-storj)


## User API calls overview


| Command               | Arguments                         | Returns   | Description                                               |
|-----------------------|-----------------------------------|-----------|-----------------------------------------------------------|
| contract_validate     | contract                          | bool      | Returns true if given object is a valid contract.         |
| contract_sign         | contract, key                     | contract  | Sign contract (all fields but signatures must be filled). |
| contract_is_complete  | contract                          | bool      | Returns true if a complete signed contract.               |
|                       |                                   |           |                                                           |
| challenge_prepare     | shardid, challenges               | leaves    | Create the corresponding leaves for the given challenges. |
| challenge_perform     | shardid, leaves, challenge        | proof     | Proof format: [[node, [leaf, [response]]], node]          |
| challenge_validate    | proof, root, challengenum, leaves | bool      | Validate that the given proof is correct.                 |
|                       |                                   |           |                                                           |
| store_import          | paths                             | shardid   | Import files/folders (behaves similar to zip).            |
| store_export          | shardid, path                     | paths     | Export a shard (behaves similar to unzip).                |
| store_add             | path                              | shardid   | Add an existing shard into the store.                     |
| store_remove          | shardid                           |           | Remove a shard from the store.                            |


## User API argument/return data structures

| Name         | Format                                                         |
|--------------|----------------------------------------------------------------|
| contract     | JSON serializable [contract](contract).                        |
| key          | Private key in bitcoin wif or hwif format.                     |
| shardid      | 256bit hex encoded hash of shard.                              |
| challenge    | { "seed": 256bit_hex_encoded, "offset": int, "size": int }     |
| root         | 256bit hex encoded merkle root                                 |
| leaf         | 256bit hex encoded leaf of merkle tree                         |
| node         | 256bit hex encoded node of merkle tree                         |
| response     | 256bit hex encoded challenge response that hashes to a leaf    |
| proof        | [[node, [leaf, [response]]], node]                             |


## Global hash function

All hashes are preformed with the following algorithm.

    ripemd160(sha256(data))


