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
#include <proton/container.hpp>
#include <proton/delivery.hpp>
#include <proton/message.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/receiver.hpp>
#include <proton/receiver_options.hpp>
#include <proton/source.hpp>
#include <proton/source_options.hpp>

#include <iostream>
#include <string>

struct subscribe_handler : public proton::messaging_handler {
    std::string conn_url_ {};
    std::string address_ {};
    int desired_ {0};
    int received_ {0};

    void on_container_start(proton::container& cont) override {
        cont.connect(conn_url_);
    }

    void on_connection_open(proton::connection& conn) override {
        proton::receiver_options opts {};
        proton::source_options sopts {};

        std::vector<proton::symbol> caps {
            "shared",
            "global" // Global means shared across clients (distinct container IDs)
        };

        sopts.capabilities(caps);
        sopts.durability_mode(proton::source::UNSETTLED_STATE);
        sopts.expiry_policy(proton::source::NEVER);

        opts.name("sub-1"); // A stable link name
        opts.source(sopts);
        
        conn.open_receiver(address_, opts);
    }

    void on_receiver_open(proton::receiver& rcv) override {
        std::cout << "SUBSCRIBE: Opened receiver for source address '" << address_ << "'\n";
    }

    void on_message(proton::delivery& dlv, proton::message& msg) override {
        std::cout << "SUBSCRIBE: Received message '" << msg.body() << "'\n";

        received_++;

        if (received_ == desired_) {
            dlv.receiver().detach(); // Detaching leaves the subscription intact
            dlv.connection().close();
        }
    }
};

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) {
        std::cerr << "Usage: durable-shared-subscribe <connection-url> <address> [<message-count>]\n";
        return 1;
    }

    subscribe_handler handler {};
    handler.conn_url_ = argv[1];
    handler.address_ = argv[2];

    if (argc == 4) {
        handler.desired_ = std::stoi(argv[3]);
    }

    proton::container cont {handler, "app-1"}; // A stable container ID

    try {
        cont.run();
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }

    return 0;
}
