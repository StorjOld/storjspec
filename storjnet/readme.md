# Storj network protocol layer

[Python reference implementation](https://github.com/storj/storjnet)

[node.js reference implementation](https://github.com/Storj/node-storj)


## User API Calls

| Command               | Arguments         | Returns             | Description                                           |
|-----------------------|-------------------|---------------------|-------------------------------------------------------|
| pubsub_publish        | topic, event      |                     | Publish an event on the network for a given topic.    |
| pubsub_subscribe      | topic             |                     | Subscribe to events for given topic.                  |
| pubsub_subscriptions  |                   | [topic]             | List current subscriptions.                           |
| pubsub_unsubscribe    | topic             |                     | Unsubscribe from events for given topic.              |
| pubsub_events         | topic             | [event]             | Events received for topic since last called.          |
|                       |                   |                     |                                                       |
| dht_put               | key, value        | bool                | Store key/value pair in DHT.                          |
| dht_get               | key               | value               | Get value for given key in DHT.                       |
|                       |                   |                     |                                                       |
| message_send          | nodeid, message   | bool                | Send a direct message to a known node.                |
| message_list          |                   | {nodeid: [message]} | Messages received since last called.                  |
|                       |                   |                     |                                                       |
| stream_list           |                   | {streamid: bufsize} | List currently open streams and unread bytes.         |
| stream_open           | nodeid,           | streamid            | Open a datastream with a node.                        |
| stream_close          | streamid          |                     | Close a datastream with a node.                       |
| stream_read           | streamid, data    |                     | Read from a datastream with a node.                   |
| stream_write          | streamid, len     |                     | Write to a datastream with a node.                    |


## Network RPC calls

| Command               | Arguments         | Returns             | Description                                           |
|-----------------------|-------------------|---------------------|-------------------------------------------------------|
| quasar_notify         | topic, event      |                     | TODO description                                      |
| quasar_filters        |                   | [filter]            | TODO description                                      |
|                       |                   |                     |                                                       |
| kademlia_ping         |                   |                     | TODO description                                      |
| kademlia_store        | key, value        |                     | TODO description                                      |
| kademlia_find_node    | key               |                     | TODO description                                      |
| kademlia_find_value   | key               |                     | TODO description                                      |
|                       |                   |                     |                                                       |
| message_notify        | message           |                     | TODO description                                      |
|                       |                   |                     |                                                       |
| stream_open           |                   | streamid            | Open a datastream with a node.                        |
| stream_close          | streamid          |                     | Close a datastream with a node.                       |
| stream_write          | streamid, data    | int                 | Write to a datastream with a node.                    |
