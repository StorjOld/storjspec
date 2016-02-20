
## Basic requirements

 * Scalable overlay (millions of nodes)
 * Scalable pubsub (billions of events)
 * Handles skewed pubsub data (price quotes)
 * Attack resistant pubsub (incentives exist to suppress events)


## POSSIBLE CANDIDATS


### [Combining Flexibility and Scalability in a Peer-to-Peer Publish/Subscribe System][3]

Metadata:

 * Source: Princeton/Yale, USA
 * Date: 2005
 * Overlay: Skip Graph
 * PubSub: Content-Based

Comments:

 * This has a high chance of being best paper!
 * Tested with large realistic data sets.
 * Needs to be extended to account for malitious brokers.


### [A Peer-to-Peer Approach to Content-Based Publish/Subscribe][4]

Metadata:

 * Source: Darmstadt, Germany
 * Date: 2003
 * Overlay: Chord
 * PubSub: Content-Based

Comments:

 * This has a high chance of being best paper!
 * TODO understand fully
 * TODO can be adapted to use Kademlia?


### Quasar: A Probabilistic Publish-Subscribe System for Social Networks

Metadata:

 * Source: Cornell, USA
 * Date: 2008
 * Overlay: TODO
 * PubSub: Topic-Based

Comments:

 * TODO understand fully


## UNCHECKED CANDIDATS

### [BubbleStorm: Resilient, Probabilistic, and Exhaustive Peer-to-Peer Search][8]

Metadata:

 * TODO

Comments:

 * TODO understand fully


### [Quasar: A Probabilistic Publish-Subscribe System for Social Networks][7]

Metadata:

 * TODO

Comments:

 * TODO understand fully


### [Corona: A High Performance Publish-Subscribe System for the World Wide Web][9]

Metadata:

 * TODO

Comments:

 * TODO understand fully


## UNSUATABLE CANDIDATS

### [Routing Protocol of Semantics-Based Publish/Subscribe Systems over Kademlia Network][6]

Metadata:

 * Source: Peking, China
 * Date: 2009
 * Overlay: Kademlia
 * PubSub: Semantics-Based

Comments:

 * Requires predefined atomic topics (max 80).
 * No content based filtering (eg filter by price).
 * Unbalanced: Unlikely to handle skewed data sets (price quotes).


### [Content-based Publish-Subscribe Over Structured P2P Networks][5]

Metadata:

 * Source: Patras, Greece
 * Date: 2004
 * Overlay: Chord
 * PubSub: Content-Based

Comments:

 * Unbalanced: Unlikely to handle skewed data sets (price quotes).


### [Building Content-Based Publish/Subscribe Systems with Distributed Hash Tables][2]

Metadata:

 * Source: Toronto, Canada
 * Date: 2003
 * Overlay: Pastry
 * PubSub: Content-Based

Comments:

 * Content-Based to Topic-Based conversion schema may be usefull for gravety well paper.
 * Unbalanced: Unlikely to handle skewed data sets (price quotes).


### [SCRIBE: The design of a large-scale event notification infrastructure][1]

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
[6]: papers/ICBRP.pdf
[7]: papers/quasar.pdf
[8]: papers/bubblestorm.pdf
[9]: papers/corona.pdf