# Qpid Examples

## Goals

- Usable as an installable test suite that can target different
  intermediaries

## Content outline

- Primary examples
  - [sender](#sender)
  - [receiver](#receiver)
  - [requester](#requester)
  - [responder](#responder)
- Peer-to-peer examples
  - [listening-receiver](#listening-receiver) - Works with sender
  - [listening-responder](#listening-responder) - Works with requester
- Error handling and logging
- AMQP type conversion
- Interop with JMS
- Additional topics
  - Transactions
  - Multithreading
  - IO integration
  - Message selectors
  - Timers
  - Reconnect
  - Codec

## General properties

- Sending programs send one message and then exit.

- By default, receiving programs keep running until the user
  terminates them.  If the optional MAX-COUNT argument is supplied,
  they exit after the given number of messages have been received.

## Sender

Usage: `sender ADDRESS MESSAGE`

        $ python sender.py amqpdemo.net/examples "Hello there"
        SENDER: Created sender for target address 'amqpdemo.net/examples'
        SENDER: Sent message 'Hello there'

## Receiver

Usage: `receiver ADDRESS [MAX-COUNT]`

        $ python receiver.py amqpdemo.net/examples
        RECEIVER: Created receiver for source address 'amqpdemo.net/examples'
        RECEIVER: Received message 'Hello there'

## Requester

Usage: `requester ADDRESS MESSAGE`

        $ python requester.py amqpdemo.net/examples "abcdef"
        REQUESTER: Created sender for target address 'amqpdemo.net/examples'
        REQUESTER: Created receiver using a dynamic reply address
        REQUESTER: Sent request message 'abcdef'
        REQUESTER: Received response message 'ABCDEF'

## Responder

Usage: `responder ADDRESS [MAX-COUNT]`

        $ python responder.py amqpdemo.net/examples
        RESPONDER: Created receiver for source address 'amqpdemo.net/examples'
        RESPONDER: Received request message 'abcdef'
        RESPONDER: Sent response message 'ABCDEF'
