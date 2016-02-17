# Storj network protocol layer

[Python reference implementation](https://github.com/storj/storjnet)
[node.js reference implementation](https://github.com/Storj/node-storj)


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


## Basic requirements

 * Scalable overlay (millions of nodes)
 * Scalable pubsub (billions of events)
 * Content based pubsub (filter by price)
 * Handles skewed pubsub (stock quotes)
 * Attack resistant pubsub (incentives exist to suppress events)


## POSSIBLE CANDIDATS

### [Distributed Semantic Algorithm for Power Constrained Publish/Subscribe Routing][1]    

Metadata:

 * Source: Oulu, Finnland        
 * Date: 2010  
 * Overlay: TODO
 * PubSub: TODO

Comments:

 * TODO understand fully


### [Combining Flexibility and Scalability in a Peer-to-Peer Publish/Subscribe System][3]    

Metadata:

 * Source: Princeton/Yale, USA   
 * Date: 2005  
 * Overlay: Skip Graph
 * PubSub: Content-Based

Comments:

 * This has a high chance of being best paper!
 * Needs to be extended to account for malitious brokers.


### [Content-based Publish-Subscribe Over Structured P2P Networks][4]    

Metadata:

 * Source: Patras, Greece        
 * Date: 2004  
 * Overlay: Chord
 * PubSub: Content-Based

Comments:

 * TODO understand fully


### [A Peer-to-Peer Approach to Content-Based Publish/Subscribe][5]    

Metadata:

 * Source: Darmstadt, Germany    
 * Date: 2003  
 * Overlay: Chord
 * PubSub: Content-Based

Comments:

 * This has a high chance of being best paper!
 * TODO understand fully
 * TODO can be adapted to use Kademlia?


### [Building Content-Based Publish/Subscribe Systems with Distributed Hash Tables][6]    

Metadata:

 * Source: Toronto, Canada       
 * Date: 2003  
 * Overlay: Pastry
 * PubSub: Content-Based

Comments:

 * TODO understand fully


## UNSUATABLE CANDIDATS

### [Routing Protocol of Semantics-Based Publish/Subscribe Systems over Kademlia Network][2]    

Metadata:

 * Source: Peking, China         
 * Date: 2009  
 * Overlay: Kademlia
 * PubSub: Semantics-Based

Comments:

 * Requires predefined atomic topics (max 80).
 * No content based filtering (eg filter by price).
 * Unlikely to handle skewed data sets (price quotes).


### [SCRIBE: The design of a large-scale event notification infrastructure][7]    

Metadata:

 * Source: Microsoft             
 * Date: 2001  
 * Overlay: Pastry
 * PubSub: Topic-Based

Comments:

 * No content based filtering (eg filter by price).


[1]: papers/scribe.pdf
[2]: papers/toronto.pdf
[3]: papers/princeton_yale.pdf
[4]: papers/darmstadt.pdf
[5]: papers/petras.pdf
[6]: papers/oulu.pdf
[7]: papers/ICBRP.pdf
