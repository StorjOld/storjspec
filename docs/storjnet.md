# Storj network protocol layer

[Python reference implimentation](https://github.com/storj/storjnet)

## User API

| Command       | Arguments                   | Returns             | Raises                        | Description                                                   |
|---------------|-----------------------------|---------------------|-------------------------------|---------------------------------------------------------------|
| publish       | event                       |                     | InvalidEvent                  | Publish an event on the network.                              |
| subscribe     | schema                      |                     | InvalidSchema                 | Subscribe to matching events.                                 |
| subscriptions |                             | [schema]            |                               | List current subscriptions.                                   |
| unsubscribe   | schema                      |                     | InvalidSchema                 | Unsubscribe from matching events.                             |
| events        | schema                      | [event]             | InvalidSchema                 | Events received for subscription since last called.           | 
|               |                             |                     |                               |                                                               |
| message       | nodeid, ip, port, message   | bool                | InvalidMessage, InvalidNodeid | Send a direct message to a known node.                        | 
| messages      |                             | {nodeid: [message]} |                               | Messages received since last called.                          |
|               |                             |                     |                               |                                                               |
| streams       |                             | {streamid: bufsize} |                               | List currently open streams and unread bytes.                 |
| open          | nodeid, ip, port            | streamid            | TODO                          | Open a datastream with a node.                                |
| close         | streamid                    |                     | TODO                          | Close a datastream with a node.                               |
| read          | streamid, data              |                     | TODO                          | Read from a datastream with a node.                           |
| write         | streamid, len               |                     | TODO                          | Write to a datastream with a node.                            |

