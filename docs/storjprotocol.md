# Storj core protocol layer

[Python reference implimentation](https://github.com/storj/storjprotocol)


## Contract version 0 specification

| Property          |      Type                         |
|-------------------|:---------------------------------:|
| version           | int=0                             |
| renterid          | 160bit                            |
| farmerid          | 160bit                            |
| shardid           | 160bit                            |
| time_begin        | 64Bit Unixtime                    |
| time_duration     | 64Bit Unixtime                    |
| payment_currency  | 64Bit Unixtime                    |
| payment_amount    | 64Bit Unixtime                    |
| audit_points      | [(64Bit Unixtime, value), ...]    |

