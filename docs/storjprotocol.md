# Storj core protocol layer

[Python reference implimentation](https://github.com/storj/storjprotocol)


## Contract version 0 specification

| Property  |      Type             | Description                               |
|-----------|:---------------------:|:-----------------------------------------:|
| version   | int=0                 |                                           |
| renterid  | 160bit                |                                           |
| farmerid  | 160bit                |                                           |
| shardid   | 160bit                |                                           |
| begin     | 64Bit Unixtime        | When the contract begins                  |
| end       | 64Bit Unixtime        | When the contract ends                    |
| currency  | integer               |                                           |
| amount    | integer               |                                           |
| audits    | [(float, float), ...] | Relative (time, amount), sum must be 1.0  |

