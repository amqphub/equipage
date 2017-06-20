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
    def __init__(self, address):
        super(Handler, self).__init__()

        self.address = address
        
        self.sender = None
        self.receiver = None

    def on_connection_opened(self, event):
        self.receiver = event.container.create_receiver(event.connection, self.address)
        self.sender = event.container.create_sender(event.connection, None)

    def on_message(self, event):
        request = event.message
        id_ = event.container.container_id
        
        print("{}: Received request '{}'".format(id_, request.body))

        body = "{} [{}]".format(request.body.upper(), id_)

        response = Message(body)
        response.address = request.reply_to
        response.correlation_id = request.correlation_id

        self.sender.send(response)
        
        print("{}: Sent response '{}'".format(id_, response.body))
        
if __name__ == "__main__":
    server = sys.argv[1];
    address = sys.argv[2];
    id_ = sys.argv[3];

    container = Container(Handler(address))
    container.container_id = id_
    container.connect(server, allowed_mechs=b"ANONYMOUS")
    container.run()
