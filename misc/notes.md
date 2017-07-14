
 - Artemis
   - Setting up queues

 - AMQP
   - Connection, Session, Link
     - Declarative state exchange
     - Pipelining
   - Credit-based flow control
   - Type system
   - Reference links

 - Java JMS (Qpid JMS)
   - Setting up connection factory
   - Send and receive example using Artemis
   - Multiple receivers with a topic
   - Address flow control here (through config?)
   - PN_TRACE_FRM
   - Reference links
     - Home, config reference

 - Node.js (Rhea)
   - Request-response example using Dispatch router
     - Or direct?
   - 

## Todo

 - Fix slf4j warning
 - Fix even-odd send problem

## Requested topics from Jason Sherman

 - example of api usage patterns for queues, topics, request-reply, etc.
 - any common usage mistakes
 - quick explanation of flow control credit and how it works/configure in both APIs
 - activating transport logging for tracing/debugging
 - explanation of the protocol messages on the wire
 - correctly setting properties for the examples in qpid-client-cpp
 
