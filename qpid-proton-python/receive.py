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

from proton.handlers import MessagingHandler
from proton.reactor import Container

class ReceiveHandler(MessagingHandler):
    def __init__(self, conn_url, address, count):
        super(ReceiveHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address
        self.count = count

        self.received = 0
        self.stopping = False

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)
        event.container.create_receiver(conn, self.address)

    def on_connection_opened(self, event):
        print("RECEIVE: Connected to '{0}'".format(self.conn_url))

    def on_link_opened(self, event):
        print("RECEIVE: Created receiver for source address '{0}'".format(self.address))

    def on_message(self, event):
        if self.stopping:
            return

        message = event.message
        
        print("RECEIVE: Received message '{0}'".format(message.body))

        self.received += 1

        if self.received == self.count:
            event.connection.close()
            self.stopping = True

def main():
    try:
        conn_url, address = sys.argv[1:3]
    except IndexError:
        sys.exit("Usage: receive.py CONNECTION-URL ADDRESS [COUNT]")

    try:
        count = int(sys.argv[3])
    except:
        count = 0

    handler = ReceiveHandler(conn_url, address, count)
    container = Container(handler)
    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
