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
import uuid

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

class RequestHandler(MessagingHandler):
    def __init__(self, conn_url, address, message_body):
        super(RequestHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address

        try:
            self.message_body = unicode(message_body)
        except NameError:
            self.message_body = message_body

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)

        self.sender = event.container.create_sender(conn, self.address)
        event.container.create_receiver(conn, None, dynamic=True)

    def on_link_opened(self, event):
        if event.link.is_sender:
            print("REQUEST: Opened sender for target address '{0}'".format
                  (event.sender.target.address))

        if event.link.is_receiver:
            print("REQUEST: Opened dynamic receiver for responses")

            request = Message(self.message_body)
            request.id = uuid.uuid4()
            request.reply_to = event.receiver.remote_source.address

            self.sender.send(request)

            print("REQUEST: Sent request '{0}'".format(request.body))

    def on_message(self, event):
        message = event.message

        print("REQUEST: Received response '{0}'".format(message.body))

        event.receiver.close()
        event.connection.close()

def main():
    try:
        conn_url, address, message_body = sys.argv[1:4]
    except ValueError:
        sys.exit("Usage: request.py <connection-url> <address> <message-body>")

    handler = RequestHandler(conn_url, address, message_body)
    container = Container(handler)
    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
