# Storj network protocol layer

[Python reference implimentation](https://github.com/storj/storjnet)


## User API Calls

| Command               | Arguments                   | Returns             | Description                                                   |
|-----------------------|-----------------------------|---------------------|---------------------------------------------------------------|
| pubsub_publish        | event                       |                     | Publish an event on the network.                              |
| pubsub_subscribe      | schema                      |                     | Subscribe to matching events.                                 |
| pubsub_subscriptions  |                             | [schema]            | List current subscriptions.                                   |
| pubsub_unsubscribe    | schema                      |                     | Unsubscribe from matching events.                             |
| pubsub_events         | schema                      | [event]             | Events received for subscription since last called.           | 
|                       |                             |                     |                                                               |
| message_send          | nodeid, ip, port, message   | bool                | Send a direct message to a known node.                        | 
| message_list          |                             | {nodeid: [message]} | Messages received since last called.                          |
|                       |                             |                     |                                                               |
| stream_list           |                             | {streamid: bufsize} | List currently open streams and unread bytes.                 |
| stream_open           | nodeid, ip, port            | streamid            | Open a datastream with a node.                                |
| stream_close          | streamid                    |                     | Close a datastream with a node.                               |
| stream_read           | streamid, data              |                     | Read from a datastream with a node.                           |
| stream_write          | streamid, len               |                     | Write to a datastream with a node.                            |

