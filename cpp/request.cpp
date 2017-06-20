/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */

#include <proton/connection.hpp>
#include <proton/connection_options.hpp>
#include <proton/container.hpp>
#include <proton/default_container.hpp>
#include <proton/delivery.hpp>
#include <proton/link.hpp>
#include <proton/message.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/thread_safe.hpp>
#include <proton/tracker.hpp>
#include <proton/receiver_options.hpp>
#include <proton/source_options.hpp>

#include <iostream>
#include <string>

struct handler : public proton::messaging_handler {
    std::string address;
    std::string data;

    proton::sender sender;
    proton::receiver receiver;

    void on_connection_open(proton::connection& conn) override {
        sender = conn.open_sender(address);

        proton::receiver_options opts;
        opts.source(proton::source_options().dynamic(true));

        receiver = conn.open_receiver("", opts);
    }

    void on_receiver_open(proton::receiver& rcv) override {
        proton::message request = proton::message(data);
        request.reply_to(rcv.source().address());

        sender.send(request);

        std::cout << "request.cpp: Sent request '" << request.body() << "'" << std::endl;
    }

    void on_message(proton::delivery& dlv, proton::message& response) override {
        std::cout << "request.cpp: Received response '" << response.body() << "'" << std::endl;

        dlv.connection().close();
    }
};

int main(int argc, char** argv) {
    std::string server = argv[1];

    handler h;
    h.address = argv[2];
    h.data = argv[3];

    proton::default_container container(h);

    proton::connection_options opts;
    opts.sasl_allowed_mechs("ANONYMOUS");

    container.connect(server, opts);
    container.run();

    return 0;
}
