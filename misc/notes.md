# Notes

## All examples

 - Provide usage.
 - Use accessors for logged values rather than using a saved input.

## C++ style

 - In general, use "\n", not std::endl.
 - Use override.
 - Use auto.
 - Use uniform initialization.
 - Use standard var names - cont, conn, ssn, snd, rcv, src, tgt, dlv, trk, err, opts, trans, handler.
 - Use a single trailing underscore for member var names.
 - Use #include per class.

## JavaScript style

 - Use var names with underbars, not studly caps.
 - Don't use quotes on dictionary keys.

## Todo

 - Fix slf4j warning
 - Fix even-odd send problem

## Requested topics from Jason Sherman

 - Example of api usage patterns for queues, topics, request-reply, etc.
 - Any common usage mistakes
 - Quick explanation of flow control credit and how it works/configure in both APIs
 - Activating transport logging for tracing/debugging
 - Explanation of the protocol messages on the wire
 - Correctly setting properties for the examples in qpid-client-cpp
 
## Unfiled

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
