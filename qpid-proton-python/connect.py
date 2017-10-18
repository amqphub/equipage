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

class ConnectHandler(MessagingHandler):
    def __init__(self, connection_url):
        super(ConnectHandler, self).__init__()

        self.connection_url = connection_url
    
    def on_start(self, event):
        event.container.connect(self.connection_url)

    def on_connection_opened(self, event):
        print("CONNECT: Connected to '{0}'".format(self.connection_url))

        event.connection.close()

def main():
    try:
        connection_url = sys.argv[1]
    except:
        sys.exit("Usage: connect.py CONNECTION-URL")

    handler = ConnectHandler(connection_url)
    container = Container(handler)
    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
