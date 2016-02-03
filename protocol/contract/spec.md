# Storage contract

* Establishes a relationship between farmer and renter
* Defines behavior pattern for storage
* One party creates contract proposal
* Bid/Ask is broadcast to the network
* Prospective partner responds with signed counteroffer
* Once both parties sign the same version, contract is complete
* Proceed to handshake for file transfer 


## Contract validation

 * A contract is valid (not complete) if it matches the [schema](schema.json).
 * A contract is complete if all fields are filled (not `null`).
 * The signatures cover all fields excluding signaturs in alphanumeric order.


## Contract fields

| Property                  | Type                  | Description                               |
|---------------------------|:---------------------:|:-----------------------------------------:|
| version                   | string                | Random 256bit hex encoded id.             |
|                           |                       |                                           |
| renter_id                 | string                | 160bit base58 encoded (bitcoin address)   |
| renter_address            | string                | IPv4 or IPv6 or hostname                  |
| renter_port               | integer               | 0 < port < 65535                          |
| renter_signature          | string                | 65byte base64 encoded bitcoin signature   |
| farmer_id                 | string                | 160bit base58 encoded (bitcoin address)   |
| farmer_address            | string                | IPv4 or IPv6 or hostname                  |
| farmer_port               | integer               | 0 < port < 65535                          |
| farmer_signature          | string                | 65byte base64 encoded bitcoin signature   |
|                           |                       |                                           |
| data_size                 | integer               | In bytes as a power of two (2^size).      |
| data_hash                 | string                | Hex encoded sha256(sha256(data))          |
|                           |                       |                                           |
| store_begin               | integer               | Unixtime when the storage begins          |
| store_duration            | integer               | Storage duration in seconds               |
| store_end                 | integer               | Unixtime when the storage ends            |
|                           |                       |                                           |
| audit_algorithm           | string                | TODO document                             |
| audit_count               | string                | TODO document                             |
|                           |                       |                                           |
| payment_currency          | string                | TODO document                             |
| payment_amount            | integer               | TODO document                             |
| payment_download_price    | integer               | TODO document                             |
| payment_destination       | string                | TODO document                             |
| payment_source            | string                | TODO document                             |
| payment_settlements       | integer               | TODO document                             |
| payment_interval          | integer               | TODO document                             |


# FIXME when exactly payments are due is unclear
# TODO add ipv6 and hostname validation to schema
# TODO define initial currcencies

