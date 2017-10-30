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

struct respond_handler : public proton::messaging_handler {
    std::string conn_url_ {};
    std::string address_ {};
    int count_ {1};

    proton::sender sender_ {};
    int received_ {0};
    bool stopping_ {false};

    void on_container_start(proton::container& cont) override {
        cont.connect(conn_url_);
    }
    
    void on_connection_open(proton::connection& conn) override {
        conn.open_receiver(address_);
        sender_ = conn.open_sender("");
    }

    void on_message(proton::delivery& dlv, proton::message& request) override {
        if (stopping_) return;

        std::cout << "RESPOND: Received request '" << request.body() << "'\n";

        auto body = proton::get<std::string>(request.body());
        std::transform(body.begin(), body.end(), body.begin(), ::toupper);

        proton::message response {body};
        response.to(request.reply_to());
        response.correlation_id(request.correlation_id());

        sender_.send(response);

        std::cout << "RESPOND: Sent response '" << response.body() << "'\n";

        received_++;

        if (received_ == count_) {
            dlv.connection().close();
            stopping_ = true;
        }
    }
};

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) {
        std::cerr << "Usage: respond CONNECTION-URL ADDRESS [COUNT]\n";
        return 1;
    }

    respond_handler handler {};
    handler.conn_url_ = argv[1];
    handler.address_ = argv[2];

    if (argc == 4) {
        handler.count_ = std::stoi(argv[3]);
    }

    proton::container cont {handler};
    cont.run();

    return 0;
}
