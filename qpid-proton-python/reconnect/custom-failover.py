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
import time

from proton import *
from proton.handlers import *
from proton.reactor import *

class Handler(MessagingHandler):
    def __init__(self, servers):
        super(Handler, self).__init__()

        self.servers = servers
        self.current_server_index = 0

        self.conn = None

    def current_server(self):
        return self.servers[self.current_server_index]

    def connect(self, event):
        print("Connecting to {0}".format(self.current_server()))

        self.conn = event.container.connect(self.current_server())

    def on_start(self, event):
        self.connect(event)

    def on_connection_opened(self, event):
        print("Connected to {0}".format(self.current_server()))

    def on_disconnected(self, event):
        print("Disconnected from {0}".format(self.current_server()))

        self.conn.close()

        self.current_server_index += 1

        if self.current_server_index == len(self.servers):
            self.current_server_index = 0

        self.connect(event)

def main():
    servers = sys.argv[1:]

    handler = Handler(servers)
    container = Container(handler)

    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
