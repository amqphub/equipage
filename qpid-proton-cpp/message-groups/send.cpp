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
#include <proton/message.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/sender.hpp>
#include <proton/target.hpp>

#include <iostream>
#include <string>

struct send_handler : public proton::messaging_handler {
    std::string conn_url_ {};
    std::string address_ {};
    int count_ {0};
    std::string group_id_ {};

    void on_container_start(proton::container& cont) override {
        proton::connection conn = cont.connect(conn_url_);
        conn.open_sender(address_);
    }

    void on_sender_open(proton::sender& snd) override {
        std::cout << "SEND: Opened sender for target address '"
                  << snd.target().address() << "'\n";
    }

    void on_sendable(proton::sender& snd) override {
        for (int i = 0; i < count_; i++) {
            proton::message msg { "message-" + std::to_string(i) };

            msg.group_id(group_id_);
            msg.group_sequence(i);

            snd.send(msg);

            std::cout << "SEND: Sent message '" << msg.body() << "'"
                      << " in group '" << msg.group_id() << "'"
                      << " with sequence number " << msg.group_sequence() << "\n";
        }

        snd.close();
        snd.connection().close();
    }
};

int main(int argc, char** argv) {
    if (argc != 5) {
        std::cerr << "Usage: send <connection-url> <address> <message-count> <group-id>\n";
        return 1;
    }

    send_handler handler {};
    handler.conn_url_ = argv[1];
    handler.address_ = argv[2];
    handler.count_ = std::stoi(argv[3]);
    handler.group_id_ = argv[4];

    proton::container cont {handler};

    try {
        cont.run();
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }

    return 0;
}
