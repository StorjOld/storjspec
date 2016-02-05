# Storage contract

A storage contract defines obligations between farmer and renter.


## Contract rules

 * A contract is valid (not complete) if it matches the [schema](schema.json).
 * A contract is complete if all fields are filled (not `null`).
 * The signatures cover all fields excluding signatures serialized in alphanumeric order.

## Establishing a binding contract

 * One party creates an incomplete bid/ask contract and publishes on the network.
 * Prospective partner responds with signed counteroffer.
 * Counteroffers continue until both parties signed a complete contract which is then binding.


## Contract fields

TODO add ipv6 and hostname validation to schema

| Property                  | Type                  | Description                                                           |
|---------------------------|:---------------------:|:---------------------------------------------------------------------:|
| type                      | string                | "56ce3e837f575827cb5a94e2b609756a48fa4a3882f5e762b262af31f432878d"    |
|                           |                       |                                                                       |
| renter_id                 | string                | 160bit base58 encoded bitcoin address (do not used for payments!)     |
| renter_address            | string                | IPv4 or IPv6 or hostname                                              |
| renter_port               | integer               | 0 < port <= 65535                                                     |
| renter_signature          | string                | 65byte base64 encoded bitcoin signature                               |
| farmer_id                 | string                | 160bit base58 encoded bitcoin address (do not used for payments!)     |
| farmer_address            | string                | IPv4 or IPv6 or hostname                                              |
| farmer_port               | integer               | 0 < port <= 65535                                                     |
| farmer_signature          | string                | 65byte base64 encoded bitcoin signature                               |
|                           |                       |                                                                       |
| data_size                 | integer               | In bytes as a power of two (2^size).                                  |
| data_hash                 | string                | Hex encoded sha256(sha256(data))                                      |
|                           |                       |                                                                       |
| store_begin               | integer               | Unixtime when the storage begins                                      |
| store_duration            | integer               | Storage duration in seconds                                           |
| store_end                 | integer               | Unixtime when the storage ends                                        |
|                           |                       |                                                                       |
| audit_algorithm           | string                | TODO document                                                         |
| audit_count               | integer               | TODO document                                                         |
| audit_merkle_root         | string                | Hex encoded 256bit merkle root of audit merkle tree.                  | 
|                           |                       |                                                                       |
| heartbeat_algorithm       | string                | TODO document                                                         |
| heartbeat_interval        | integer               | Seconds between heartbeats                                            |
| heartbeat_coverage        | integer               | Size of data covered by a heartbeat in bytes                          |
|                           |                       |                                                                       |
| payment_currency          | string                | TODO document                                                         |
| payment_amount            | integer               | TODO document                                                         |
| payment_download_price    | integer               | Price per download of stored data.                                    |
| payment_destination       | string                | Payment information needed to pay to farmer.                          |
| payment_source            | string                | Payment information needed to pay to renter (negative payment).       |
| payment_begin             | integer               | Unixtime of first payment                                             |
| payment_settlements       | integer               | Number of payments to be made.                                        |
| payment_interval          | integer               | The interval in which payments are made.                              |





# TODO define initial currencies
