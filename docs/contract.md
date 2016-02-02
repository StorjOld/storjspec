Contracts
=========

What does a contract do?

* Establishes a relationship between farmer and renter
* Defines behavior pattern for storage
* One party creates contract proposal
* Bid/Ask is broadcast to the network
* Prospective partner responds with signed counteroffer
* Once both parties sign the same version, contract is complete
* Proceed to handshake for file transfer 

What does a contract need?
* version : int
* shard size : int
* duration
  * start : int
  * storage duration : int
* hash of shard : String
* parties
  * renter node contact
    * node id : string
    * ip : string
    * port : int
  * farmer node contact
    * node id : string
    * ip : string
    * port : int
* payment strategy
  * version : int
  * strategy description
    * unit : String
    * amount : int
    * destination : ?
    * source : ?
    * download price : int
    * settlement time
      * number of settlements : int
      * interval : int
* audit strategy
  * audit algorithm : 
  * audit timing
    * number of audits : int
    * interval : int


Future expansions?
* more parties
* 


