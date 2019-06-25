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
require 'securerandom'

class RequestHandler < Qpid::Proton::MessagingHandler
  def initialize(conn_url, address, message_body)
    super()

    @conn_url = conn_url
    @address = address
    @message_body = message_body
  end

  def on_container_start(container)
    conn = container.connect(@conn_url)

    @sender = conn.open_sender(@address)
    conn.open_receiver({:dynamic => true})
  end

  def on_sender_open(sender)
    puts "REQUEST: Opened sender for target address '#{sender.target.address}'\n"
  end

  def on_receiver_open(receiver)
    puts "REQUEST: Opened dynamic receiver for responses\n"

    request = Qpid::Proton::Message.new(@message_body)
    request.id = SecureRandom.uuid
    request.reply_to = receiver.remote_source.address

    @sender.send(request)

    puts "REQUEST: Sent request '#{request.body}'\n"
  end

  def on_message(delivery, message)
    puts "REQUEST: Received response '#{message.body}'\n"

    delivery.receiver.close
    delivery.receiver.connection.close
  end
end

if ARGV.size == 3
  conn_url, address, message_body = ARGV
else
  abort "Usage: request.rb <connection-url> <address> <message-body>\n"
end

handler = RequestHandler.new(conn_url, address, message_body)
container = Qpid::Proton::Container.new(handler)
container.run
