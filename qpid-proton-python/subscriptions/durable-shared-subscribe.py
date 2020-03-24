#!/usr/bin/python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import print_function

import sys

from proton import symbol, Terminus
from proton.handlers import MessagingHandler
from proton.reactor import Container, ReceiverOption

class SubscribeHandler(MessagingHandler):
    def __init__(self, conn_url, address, desired):
        super(SubscribeHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address

        self.desired = desired
        self.received = 0

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)

        # Set the receiver name to a stable value, such as "sub-1"
        event.container.create_receiver(conn, self.address, name="sub-1",
                                        options=SubscriptionOptions())

    def on_link_opened(self, event):
        print("SUBSCRIBE: Opened receiver for source address '{0}'".format
              (event.receiver.source.address))

    def on_message(self, event):
        message = event.message

        print("SUBSCRIBE: Received message '{0}'".format(message.body))

        self.received += 1

        if self.received == self.desired:
            # Detaching the receiver instead of closing it leaves the
            # subscription intact
            event.receiver.detach()

            event.connection.close()

# Configure the receiver source for durability
class SubscriptionOptions(ReceiverOption):
    def apply(self, receiver):
        # Global means shared across clients (distinct container IDs)
        receiver.source.capabilities.put_object(symbol("shared"))
        receiver.source.capabilities.put_object(symbol("global"))

        # Preserve unsettled delivery state
        receiver.source.durability = Terminus.DELIVERIES

        # Don't expire the source
        receiver.source.expiry_policy = Terminus.EXPIRE_NEVER

def main():
    try:
        conn_url, address = sys.argv[1:3]
    except ValueError:
        sys.exit("Usage: durable-subscribe.py <connection-url> <address> [<message-count>]")

    try:
        desired = int(sys.argv[3])
    except (IndexError, ValueError):
        desired = 0

    handler = SubscribeHandler(conn_url, address, desired)
    container = Container(handler)

    # Set the container ID to a stable value, such as "client-1"
    container.container_id = "client-1"

    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
