#!/usr/bin/env ruby
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

require 'qpid_proton'

class ConnectHandler < Qpid::Proton::MessagingHandler
  def initialize(conn_url)
    super()

    @conn_url = conn_url
  end

  def on_container_start(container)
    container.connect(@conn_url)

    # To connect with a user and password:

    # container.connect(@conn_url, { :user => "alice", :password => "secret" })

    # Use `:sasl_allow_insecure_mechs => true` to connect with a user
    # and password over a non-TLS connection.
  end

  def on_connection_open(conn)
    puts "CONNECT: Connected to '#{@conn_url}'\n"
    conn.close()
  end
end

if ARGV.size == 1
  conn_url = ARGV[0]
else
  abort "Usage: connect.rb <connection-url>\n"
end

handler = ConnectHandler.new(conn_url)
container = Qpid::Proton::Container.new(handler)
container.run
