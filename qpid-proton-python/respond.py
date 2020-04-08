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
from __future__ import unicode_literals

import sys

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

class RespondHandler(MessagingHandler):
    def __init__(self, conn_url, address, desired):
        super(RespondHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address

        self.desired = desired
        self.received = 0

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)

        event.container.create_receiver(conn, self.address)
        self.sender = event.container.create_sender(conn, None)

    def on_link_opened(self, event):
        if event.link.is_sender:
            print("RESPOND: Opened anonymous sender for responses")

        if event.link.is_receiver:
            print("RESPOND: Opened receiver for source address '{0}'".format
                  (event.receiver.source.address))

    def on_message(self, event):
        request = event.message

        print("RESPOND: Received request '{0}'".format(request.body))

        response_body = request.body.upper()

        response = Message(response_body)
        response.address = request.reply_to
        response.correlation_id = request.id

        self.sender.send(response)

        print("RESPOND: Sent response '{0}'".format(response.body))

        self.received += 1

        if self.received == self.desired:
            event.receiver.close()
            event.connection.close()

def main():
    try:
        conn_url, address = sys.argv[1:3]
    except ValueError:
        sys.exit("Usage: respond.py <connection-url> <address> [<message-count>]")

    try:
        desired = int(sys.argv[3])
    except (IndexError, ValueError):
        desired = 0

    handler = RespondHandler(conn_url, address, desired)
    container = Container(handler)
    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
