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

import sys

from proton import *
from proton.handlers import *
from proton.reactor import *

class Sender(MessagingHandler):
    def __init__(self, address, message_body):
        super(Sender, self).__init__()

        self.address = address
        self.message_body = message_body

        self.sent = False
    
    def on_start(self, event):
        event.container.create_sender(self.address)

        print("SENDER: Created sender for target address '{0}'".format(self.address))

    def on_sendable(self, event):
        if self.sent:
            return

        message = Message(self.message_body)
        event.sender.send(message)

        print("SENDER: Sent message '{0}'".format(self.message_body))
        
        event.connection.close()

        self.sent = True
        
try:
    address, message_body = sys.argv[1:]
except:
    sys.exit("Usage: sender.py ADDRESS MESSAGE")

handler = Sender(address, message_body)
container = Container(handler)

try:
    container.run()
except KeyboardInterrupt:
    pass
