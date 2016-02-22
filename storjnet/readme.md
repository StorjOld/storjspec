# Storj network protocol layer


Reference implements:

 * [Python](https://github.com/storj/storjnet)
 * [node.js](https://github.com/Storj/node-storj)


Algorithms:

 * Publish/Subscribe: [Quasar](http://www.cs.toronto.edu/iptps2008/final/70.pdf)
 * Distributed hash table: [Kademlia](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf)
 * Direct Messaging: Simple rpc calls
 * Data streams: Simple rpc call


## User API Calls

| Command               | Arguments         | Returns                       | Description                                           |
|-----------------------|-------------------|-------------------------------|-------------------------------------------------------|
| dht_put               | key, value        | bool                          | Store key/value pair in DHT.                          |
| dht_get               | key               | value                         | Get value for given key in DHT.                       |
| dht_find              | nodeid            | [ip, port]                    | Get [ip, port] of node if online.                     |
|                       |                   |                               |                                                       |
| pubsub_publish        | topic, event      |                               | Publish an event on the network for a given topic.    |
| pubsub_subscribe      | topic             |                               | Subscribe to events for given topic.                  |
| pubsub_subscriptions  |                   | [topic]                       | List current subscriptions.                           |
| pubsub_unsubscribe    | topic             |                               | Unsubscribe from events for given topic.              |
| pubsub_events         | topic             | [event]                       | Events received for topic since last called.          |
|                       |                   |                               |                                                       |
| message_send          | nodeid, message   | bool                          | Send a direct message to a known node.                |
| message_list          |                   | {nodeid: [message]}           | Messages received since last called (in order).       |
|                       |                   |                               |                                                       |
| stream_list           |                   | {streamid: [nodeid, size]}    | List open streams and size of unread bytes.           |
| stream_open           | nodeid,           | streamid                      | Open a datastream with a node.                        |
| stream_close          | streamid          |                               | Close a datastream with a node.                       |
| stream_read           | streamid, size    | data                          | Read from a datastream with a node.                   |
| stream_write          | streamid, data    |                               | Write to a datastream with a node.                    |


## Network RPC calls

All rpc calls have the following implied arguments:

 * netid
 * caller [id, ip, port]
 * signature

FIXME reading/writing data is going to be fuck slow if everything has to be signed/validated

| Command               | Arguments                     | Returns       | Description                                           |
|-----------------------|-------------------------------|---------------|-------------------------------------------------------|
| quasar_filters        |                               | [filter]      | Paper: Algorithm 1 line 8                             |
| quasar_update         | [filter]                      |               | Paper: Algorithm 1 line 12                            |
| quasar_notify         | topic, event, ttl, publishers |               | Paper: Algorithm 2 line 8, 21, 23                     |
|                       |                               |               |                                                       |
| kademlia_stun         |                               | [ip, port]    | TODO description                                      |
| kademlia_ping         |                               | nodeid        | TODO description                                      |
| kademlia_store        | key, value                    |               | TODO description                                      |
| kademlia_find_node    | key                           | [node]        | TODO description                                      |
| kademlia_find_value   | key                           | value         | TODO description                                      |
|                       |                               |               |                                                       |
| message_notify        | message                       | bool          | Returns false if message queue is full.               |
|                       |                               |               |                                                       |
| stream_open           |                               | streamid      | Open a datastream with a node.                        |
| stream_close          | streamid                      |               | Close a datastream with a node.                       |
| stream_write          | streamid, data                | int           | Write to a datastream with a node.                    |

