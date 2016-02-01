# Storj core protocol layer

[Python reference implimentation](https://github.com/storj/storjprotocol)


## Contract version 0 specification

| Property  |      Type             | Description                               |
|-----------|:---------------------:|:-----------------------------------------:|
| version   | int=0                 |                                           |
| renterid  | string                | 160bit base58 encoded                     |
| farmerid  | string                | 160bit base58 encoded                     |
| shardid   | string                | 160bit base58 encoded                     |
| begin     | integer               | Unixtime when the contract begins         |
| end       | integer               | Unixtime when the contract ends           |
| currency  | integer               |                                           |
| amount    | integer               |                                           |
| audits    | [(float, float), ...] | Relative (time, amount), sum must be 1.0  |

