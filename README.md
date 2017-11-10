# Messaging examples

## APIs

 - [Qpid Proton C++](http://qpid.apache.org/proton/index.html)
 - [Qpid Proton Python](http://qpid.apache.org/proton/index.html)
 - [Qpid JMS](http://qpid.apache.org/components/jms/index.html)
 - [Rhea](https://github.com/grs/rhea)

## Primary examples

 - **connect** - Connect to a messaging server
 - **send** - Send a message
 - **receive** - Receive messages
 - **request** - Send a request and receive a response
 - **respond** - Receive requests and send responses

## Connect

Usage: `connect CONNECTION-URL`

        $ python connect.py amqp://example.net
        CONNECT: Connected to 'amqp://example.net'

## Send

Usage: `send CONNECTION-URL ADDRESS MESSAGE-BODY`

        $ python send.py amqp://example.net examples "Hello there"
        SEND: Opened sender for target address 'examples'
        SEND: Sent message 'Hello there'

## Receive

Usage: `receive CONNECTION-URL ADDRESS [MESSAGE-COUNT]`

        $ python receive.py amqp://example.net examples
        RECEIVE: Opened receiver for source address 'examples'
        RECEIVE: Received message 'Hello there'

## Request

Usage: `request CONNECTION-URL ADDRESS MESSAGE-BODY`

        $ python request.py amqp://example.net examples "abcdef"
        REQUEST: Opened sender for target address 'examples'
        REQUEST: Opened receiver using a dynamic reply address # XXX
        REQUEST: Sent request message 'abcdef'
        REQUEST: Received response message 'ABCDEF'

## Respond

Usage: `respond CONNECTION-URL ADDRESS [MESSAGE-COUNT]`

        $ python respond.py amqp://example.net examples
        RESPOND: Opened receiver for source address 'examples'
        RESPOND: Received request message 'abcdef'
        RESPOND: Sent response message 'ABCDEF'

## Content outline

 - Primary examples (in the root dir)
   - connect
   - send
   - receive
   - browse
   - request
   - respond
 - Reconnect and failover (reconnect)
   - connect
   - failover
   - custom-failover
 - Authentication (authentication)
   - connect
 - Multithreaded applications (threading)
   - send
   - receive
 - Error handling (error-handling)
   - send
   - receive
 - Logging (logging)
   - send
   - receive
 - Subscriptions (subscriptions)
   - subscribe
   - durable-subscribe
   - shared-subscribe
   - durable-shared-subscribe
 - Transactions (transactions)
 - Timers (timers)
 - Filters (filters)
 - Codec (codec)
 - Interoperating with JMS (jms-interop)
 - IO integration (io-integration)

## General properties

 - The most basic sending programs send one message and then exit.

 - By default, receiving programs keep running until the user
   terminates them.  If the optional MESSAGE-COUNT argument is
   supplied, they exit after the given number of messages have been
   received.

 - Each example program is contained in a single file, with exceptions
   where necessary.

 - Option parsing is deliberately simple, using positional arguments.

## To do

 - Docs for getting dependencies
