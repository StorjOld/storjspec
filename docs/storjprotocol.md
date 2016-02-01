# Storj core protocol layer

[Python reference implimentation](https://github.com/storj/storjprotocol)


## Contract version 0 specification

| Property          |      Type                 |
|-------------------|:-------------------------:|
| version           | int=0                     |
| renterid          | 20 bytes                  |
| farmerid          | 20 bytes                  |
| shardid           | 20 bytes                  |
| time_begin        | unixtime                  |
| time_duration     | unixtime                  |
| payment_currency  | unixtime                  |
| payment_amount    | unixtime                  |
| audit_points      | [(unixtime, value), ...]  |

