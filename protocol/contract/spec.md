# Storage contract

* Establishes a relationship between farmer and renter
* Defines behavior pattern for storage
* One party creates contract proposal
* Bid/Ask is broadcast to the network
* Prospective partner responds with signed counteroffer
* Once both parties sign the same version, contract is complete
* Proceed to handshake for file transfer 


| Property                  | Type                  | Description                               |
|---------------------------|:---------------------:|:-----------------------------------------:|
| version                   | string                |                                           |
|                           |                       |                                           |
| renter_id                 | string                | 160bit base58 encoded                     |
| renter_address            | string                | IPv4 or IPv6 or domain                    |
| renter_port               | integer               | 0 <= port < 65535                         |
| farmer_id                 | string                | 160bit base58 encoded                     |
| farmer_address            | string                | IPv4 or IPv6 or domain                    |
| farmer_port               | integer               | 0 <= port < 65535                         |
|                           |                       |                                           |
| store_data_size           | integer               | In bytes as a power of two (2^size).      |
| store_data_hash           | string                | Hex encoded sha256(sha256(data))          |
| store_begin               | integer               | Unixtime when the storage begins          |
| store_duration            | integer               | Storage duration in seconds               |
| store_end                 | integer               | Unixtime when the storage ends            |
|                           |                       |                                           |
| audit_algorithm           | string                |                                           |
| audit_count               | string                |                                           |
|                           |                       |                                           |
| payment_currency          | string                |                                           |
| payment_amount            | integer               |                                           |
| payment_download_price    | integer               |                                           |
| payment_destination       | string                |                                           |
| payment_source            | string                |                                           |
| payment_settlements       | integer               |                                           |
| payment_interval          | integer               |                                           |
