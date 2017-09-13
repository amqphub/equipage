# Qpid Examples

## Naming

 - "send" - Sending in isolation
 - "receive" - Receiving in isolation
 - "request" - Sending requests and receiving responses
 - "respond" - Receiving requests and sending responses
 - "client" - Various client operations appropriate to the topic
 - <name>-<variant> for alternate versions
   - "-03" suffix for C++03 variants

## Content outline

 - Primary examples (in the root dir)
   - [hello-world](#hello-world)
   - [send](#send)
   - [receive](#receive)
   - browse
   - [request](#request)
   - [respond](#respond)
 - Reconnect and failover ("reconnect")
   - client
 - SASL authentication ("sasl")
   - client
 - TLS authentication and encryption ("tls")
   - client
 - Multithreaded ("multithreaded")
   - client
 - Error handling ("error-handling")
   - client
 - Logging ("logging")
 - Transactions ("transactions")
 - Timers ("timers")
 - Filters ("filters")
 - Servers ("servers")
   - receive - Works with primary send
   - respond - Works with primary request
   - broker
   - proxy
   - bridge
 - Codec ("codec")
 - Interoperating with JMS ("jms-interop")
 - IO integration ("io-integration")

## General properties

 - Usable as an installable test suite that can target different
   servers.

 - Sending programs send one message and then exit.

 - By default, receiving programs keep running until the user
   terminates them.  If the optional MAX-COUNT argument is supplied,
   they exit after the given number of messages have been received.

 - Each example directory is a nearly self-sufficient microcosm.
 
## Hello world

Usage: `hello-world SERVER ADDRESS`

        $ python client.py amqpdemo.net examples "Hello!"
        CLIENT: Connected to server 'amqpdemo.net'
        CLIENT: Created sender for target address 'examples'
        CLIENT: Created receiver for source address 'examples'
        CLIENT: Sent message 'Hello!'
        CLIENT: Received message 'Hello!'

## Send

Usage: `send SERVER ADDRESS MESSAGE`

        $ python send.py amqpdemo.net examples "Hello there"
        SEND: Connected to server 'amqpdemo.net'
        SEND: Created sender for target address 'examples'
        SEND: Sent message 'Hello there'

## Receive

Usage: `receive SERVER ADDRESS [MAX-COUNT]`

        $ python receive.py amqpdemo.net examples
        RECEIVE: Connected to server 'amqpdemo.net'
        RECEIVE: Created receiver for source address 'examples'
        RECEIVE: Received message 'Hello there'

## Request

Usage: `request SERVER ADDRESS MESSAGE`

        $ python request.py amqpdemo.net examples "abcdef"
        REQUEST: Connected to server 'amqpdemo.net'
        REQUEST: Created sender for target address 'examples'
        REQUEST: Created receiver using a dynamic reply address # XXX
        REQUEST: Sent request message 'abcdef'
        REQUEST: Received response message 'ABCDEF'

## Respond

Usage: `respond SERVER ADDRESS [MAX-COUNT]`

        $ python responder.py amqpdemo.net/examples
        RESPOND: Connected to server 'amqpdemo.net'
        RESPOND: Created receiver for source address 'examples'
        RESPOND: Received request message 'abcdef'
        RESPOND: Sent response message 'ABCDEF'

## Servers

Usage: `<server> SERVER ADDRESS [MAX-COUNT]`

## To do

 - Standard patterns
   - test.py or make test and scripts to support it
   - Docs for building and getting deps
