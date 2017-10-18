# Qpid Examples

## Naming

 - "send" - Sending in isolation
 - "receive" - Receiving in isolation
 - "request" - Sending requests and receiving responses
 - "respond" - Receiving requests and sending responses
 - "client" - Various client operations appropriate to the topic
 - "connect" - Making a new outbound connection

## Content outline

 - Primary examples (in the root dir)
   - connect
   - [send](#send)
   - [receive](#receive)
   - browse
   - [request](#request)
   - [respond](#respond)
 - Reconnect and failover ("reconnect")
   - client
 - Authentication ("authentication")
   - client
 - Multithreaded applications ("threading")
   - client
 - Error handling ("error-handling")
   - client
 - Logging ("logging")
 - Transactions ("transactions")
 - Timers ("timers")
 - Filters ("filters")
 - Codec ("codec")
 - Interoperating with JMS ("jms-interop")
 - IO integration ("io-integration")

## General properties

 - The most basic sending programs send one message and then exit.

 - By default, receiving programs keep running until the user
   terminates them.  If the optional MAX-COUNT argument is supplied,
   they exit after the given number of messages have been received.

 - Each example program is contained in a single file, with exceptions
   where necessary.

 - Option parsing is deliberately simple, using positional arguments.

## Send

Usage: `send CONNECTION-URL ADDRESS MESSAGE`

        $ python send.py amqpdemo.net examples "Hello there"
        SEND: Connected to 'amqpdemo.net'
        SEND: Created sender for target address 'examples'
        SEND: Sent message 'Hello there'

## Receive

Usage: `receive CONNECTION-URL ADDRESS [MAX-COUNT]`

        $ python receive.py amqpdemo.net examples
        RECEIVE: Connected to 'amqpdemo.net'
        RECEIVE: Created receiver for source address 'examples'
        RECEIVE: Received message 'Hello there'

## Request

Usage: `request CONNECTION-URL ADDRESS MESSAGE`

        $ python request.py amqpdemo.net examples "abcdef"
        REQUEST: Connected to 'amqpdemo.net'
        REQUEST: Created sender for target address 'examples'
        REQUEST: Created receiver using a dynamic reply address # XXX
        REQUEST: Sent request message 'abcdef'
        REQUEST: Received response message 'ABCDEF'

## Respond

Usage: `respond CONNECTION-URL ADDRESS [MAX-COUNT]`

        $ python responder.py amqpdemo.net/examples
        RESPOND: Connected to 'amqpdemo.net'
        RESPOND: Created receiver for source address 'examples'
        RESPOND: Received request message 'abcdef'
        RESPOND: Sent response message 'ABCDEF'

## Servers

Usage: `<server> CONNECTION-URL ADDRESS [MAX-COUNT]`

## To do

 - test.py or make test and scripts to support it
 - Docs for building and getting deps
