# Equipage

## APIs

 - [Pooled JMS](https://github.com/messaginghub/pooled-jms)
 - [Qpid JMS](http://qpid.apache.org/components/jms/index.html)
 - [Qpid Proton C++](http://qpid.apache.org/proton/index.html)
 - [Qpid Proton Python](http://qpid.apache.org/proton/index.html)
 - [Qpid Proton Ruby](http://qpid.apache.org/proton/index.html)
 - [Rhea](https://github.com/grs/rhea)
 - [Vert.x Proton](https://github.com/vert-x3/vertx-proton)

## Primary examples

 - **connect** - Connect to a messaging server
 - **send** - Send a message
 - **receive** - Receive messages
 - **request** - Send a request and receive a response
 - **respond** - Receive requests and send responses

## Connect

Usage: `connect <connection-url>`

        $ python connect.py amqp://example.net
        CONNECT: Connected to 'amqp://example.net'

## Send

Usage: `send <connection-url> <address> <message-body>`

        $ python send.py amqp://example.net examples "Hello there"
        SEND: Connected to 'amqp://example.net'
        SEND: Opened sender for target address 'examples'
        SEND: Sent message 'Hello there'

## Receive

Usage: `receive <connection-url> <address> [<message-count>]`

        $ python receive.py amqp://example.net examples
        RECEIVE: Connected to 'amqp://example.net'
        RECEIVE: Opened receiver for source address 'examples'
        RECEIVE: Received message 'Hello there'

## Request

Usage: `request <connection-url> <address> <message-body>`

        $ python request.py amqp://example.net examples "abcdef"
        REQUEST: Connected to 'amqp://example.net'
        REQUEST: Opened sender for target address 'examples'
        REQUEST: Sent request message 'abcdef'
        REQUEST: Received response message 'ABCDEF'

## Respond

Usage: `respond <connection-url> <address> [<message-count>]`

        $ python respond.py amqp://example.net examples
        RESPOND: Connected to 'amqp://example.net'
        RESPOND: Opened receiver for source address 'examples'
        RESPOND: Received request message 'abcdef'
        RESPOND: Sent response message 'ABCDEF'

## Content outline

 - Primary examples (in the root dir)
   - connect
   - send
   - receive
   - request
   - respond
 - Authentication (authentication)
   - password
   - kerberos
 - Automatic resource creation (auto-create)
   - queue-send
   - queue-receive
   - topic-send
   - topic-receive
 - Reconnect and failover (reconnect)
   - connect
   - failover
   - custom-failover
 - Servers (servers)
   - receive
   - respond
 - Subscriptions (subscriptions)
   - subscribe
   - durable-subscribe
   - shared-subscribe
   - durable-shared-subscribe
 - Codec (codec)
 - Error handling (error-handling)
 - Filters (filters)
 - IO integration (io-integration)
 - Interoperating with JMS (jms-interop)
 - Logging (logging)
 - Multithreaded applications (multithreaded)
 - Timers (timers)
 - Transactions (transactions)

## General properties

 - The most basic sending programs send one message and then exit.

 - By default, receiving programs keep running until the user
   terminates them.  If the optional MESSAGE-COUNT argument is
   supplied, they exit after the given number of messages have been
   received.

 - Each example program is contained in a single file, with exceptions
   where necessary.

 - Option parsing is deliberately simple, using positional arguments.
