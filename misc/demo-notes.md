
 - Artemis
   - Setting up queues

 - AMQP
   - Connection, Session, Link
     - Declarative state exchange
       - Pipelining
   - Credit-based flow control
   - Application-level acknowledgment and settlement
   - Type system
   - Reference links
     - http://qpid.apache.org/amqp/

 - Java JMS (Qpid JMS)
   - Setting up connection factory
   - Send and receive example using Artemis
     - Multiple receivers with a topic
   - Address flow control here (through config?)
   - PN_TRACE_FRM
   - Reference links
     - Home, config reference

 - Python (Proton Python)
   - Peer-to-peer request-response
   - PN_TRACE_FRM
   - Reference links

## Requested topics from Jason Sherman

 - example of api usage patterns for queues, topics, request-reply, etc.
 - any common usage mistakes
 - quick explanation of flow control credit and how it works/configure in both APIs
   - 
   - python credit window
 - activating transport logging for tracing/debugging
 - explanation of the protocol messages on the wire
 - correctly setting properties for the examples in qpid-client-cpp
   - qpidc.conf?
