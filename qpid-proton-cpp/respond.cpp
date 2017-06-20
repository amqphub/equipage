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
#include <proton/message_id.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/thread_safe.hpp>
#include <proton/tracker.hpp>
#include <proton/receiver_options.hpp>
#include <proton/source_options.hpp>

#include <algorithm>
#include <iostream>
#include <string>

struct handler : public proton::messaging_handler {
    std::string address;

    proton::receiver receiver;
    proton::sender sender;

    void on_connection_open(proton::connection& conn) override {
        receiver = conn.open_receiver(address);
        sender = conn.open_sender("");
    }

    void on_message(proton::delivery& dlv, proton::message& request) override {
        std::cout << dlv.container().id() << ": Received request '" << request.body() << "'" << std::endl;
        
        std::string body = proton::get<std::string>(request.body());
        std::transform(body.begin(), body.end(), body.begin(), ::toupper);
        body += " [" + dlv.container().id() + "]";
        
        proton::message response(body);
        response.to(request.reply_to());
        response.correlation_id(request.correlation_id());

        sender.send(response);

        std::cout << dlv.container().id() << ": Sent response '" << response.body() << "'" << std::endl;
    }
};

int main(int argc, char** argv) {
    std::string server = argv[1];
    std::string id = argv[3];

    handler h;
    h.address = argv[2];

    proton::default_container container(h, id);

    proton::connection_options opts;
    opts.sasl_allowed_mechs("ANONYMOUS");

    container.connect(server, opts);
    container.run();

    return 0;
}
