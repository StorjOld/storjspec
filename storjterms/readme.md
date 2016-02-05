# Storj terms specification and compatibility tests

[Python reference implimentation](https://github.com/storj/storjterms)

 * [contract](contract): A storage contract defines obligations between farmer and renter.
 * [audit](audit): Provides proof of storage.
 * [heartbeat](heartbeat): Provides proof of availability. 


## User API Calls

| Command                | Arguments                    | Returns       | Description                                                   |
|------------------------|------------------------------|---------------|---------------------------------------------------------------|
| contract_sign          | contract, key                | contract      | Sign contract (all fields except signatures must be filled.   |
| contract_is_valid      | contract                     | bool          | Returns true if given object matches the contract schema.     |
| contract_is_complete   | contract                     | bool          | Returns true if given object is a complete signed contract.   |
|                        |                              |               |                                                               |
| audit_perform          | shardid, leaves, challenge   | proof         | TODO add documentation                                        |
| audit_is_valid         | root, depth, proof           | bool          | TODO add documentation                                        |
