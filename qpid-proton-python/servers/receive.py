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

from proton.handlers import MessagingHandler
from proton.reactor import Container, ReceiverOption

class ReceiveHandler(MessagingHandler):
    def __init__(self, listen_url, address, desired):
        super(ReceiveHandler, self).__init__()

        self.listen_url = listen_url
        self.address = address

        self.desired = desired
        self.received = 0

        self.acceptor = None

    def on_start(self, event):
        self.acceptor = event.container.listen(self.listen_url)

        print("RECEIVE: Listening at {0}".format(self.listen_url))

    def on_link_opening(self, event):
        print("RECEIVE: Opening receiver for target address '{0}'".format
              (event.receiver.remote_target.address))

        # Set the target address using the value from the remote peer
        address = event.receiver.remote_target.address
        event.receiver.target.address = address

    def on_message(self, event):
        print("RECEIVE: Received message '{0}'".format(event.message.body))

        self.received += 1

        if self.received == self.desired:
            self.acceptor.close()
            event.connection.close()

def main():
    try:
        listen_url, address = sys.argv[1:3]
    except ValueError:
        sys.exit("Usage: receive.py <connection-url> <address> [<message-count>]")

    try:
        desired = int(sys.argv[3])
    except (IndexError, ValueError):
        desired = 0

    handler = ReceiveHandler(listen_url, address, desired)
    container = Container(handler)
    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
