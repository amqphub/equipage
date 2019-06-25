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

class RespondHandler < Qpid::Proton::MessagingHandler
  def initialize(conn_url, address, desired)
    super()

    @conn_url = conn_url
    @address = address

    @desired = desired
    @received = 0
  end

  def on_container_start(container)
    conn = container.connect(@conn_url)

    conn.open_receiver(@address)
    @sender = conn.open_sender({:target => nil})
  end

  def on_sender_open(sender)
    puts "RESPOND: Opened anonymous sender for responses\n"
  end

  def on_receiver_open(receiver)
    puts "RESPOND: Opened receiver for source address '#{receiver.source.address}'\n"
  end

  def on_message(delivery, message)
    puts "RESPOND: Received request '#{message.body}'\n"

    message_body = message.body.upcase

    response = Qpid::Proton::Message.new(message_body)
    response.address = message.reply_to
    response.correlation_id = message.id

    @sender.send(response)

    puts "RESPOND: Sent response '#{response.body}'\n"

    @received += 1

    if @received == @desired
      delivery.receiver.close
      delivery.connection.close
    end
  end
end

if ARGV.size > 1
  conn_url, address = ARGV[0..1]
else
  abort "Usage: respond.rb <connection-url> <address> [<message-count>]\n"
end

begin
  desired = Integer(ARGV[2])
rescue TypeError
  desired = 0
end

handler = RespondHandler.new(conn_url, address, desired)
container = Qpid::Proton::Container.new(handler)
container.run
