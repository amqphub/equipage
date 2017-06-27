#!/usr/bin/env python
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

class Handler(MessagingHandler):
    def __init__(self, address, data):
        super(Handler, self).__init__()

        self.address = address
        self.data = data

        self.sender = None
        self.receiver = None

    def on_connection_opened(self, event):
        self.sender = event.container.create_sender(event.connection, self.address)
        self.receiver = event.container.create_receiver(event.connection, None, dynamic=True)

    def on_link_opened(self, event):
        if event.receiver != self.receiver:
            return

        request = Message(unicode(self.data))
        request.reply_to = self.receiver.remote_source.address

        self.sender.send(request)

        print("request.py: Sent request '{}'".format(request.body))

    def on_message(self, event):
        print("request.py: Received response '{}'".format(event.message.body))

        event.connection.close()

if __name__ == "__main__":
    server = sys.argv[1]
    address = sys.argv[2]
    data = sys.argv[3]
    tls_enabled = False

    try:
        tls_enabled = int(sys.argv[4]) == 1
    except:
        pass

    if tls_enabled:
        server = "amqps://" + server

    container = Container(Handler(address, data))
    container.connect(server, allowed_mechs=b"ANONYMOUS")
    container.run()
