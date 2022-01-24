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
#include <proton/message_id.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/listen_handler.hpp>
#include <proton/listener.hpp>

#include <iostream>


struct receive_handler : public proton::messaging_handler {
    struct listener_ready_handler : public proton::listen_handler {
        void on_open(proton::listener& lsnr) override {
            std::cout << "RCV: listening on " << lsnr.port() << std::endl;
        }
    };

    std::string conn_url_ {};
    std::string address_ {};
    int expected_ {250};
    proton::listener listener_;
    listener_ready_handler listen_handler_;
    int received_ {0};

    void on_container_start(proton::container &cont) override {
        std::cout << "RCV: on_container_start() URL=" << conn_url_ + "/" + address_ << std::endl;
        listener_ = cont.listen(conn_url_ + "/" + address_, listen_handler_);
    }

    void on_message(proton::delivery &dlv, proton::message &msg) override {
        if (proton::coerce<int>(msg.id()) < received_) {
            return; // Ignore duplicate
        }

        if (expected_ == 0 || received_ < expected_) {
            std::cout << "RCV: " << msg.body() << std::endl;
            received_++;
        }

        if (received_ == expected_) {
            dlv.receiver().close();
            dlv.connection().close();
            listener_.stop();
        }
    }

    // Override on_receiver_error() so that default handler method is not used.
    // When the sender re-opens, the listener will automatically re-open.
    void on_receiver_error(proton::receiver &rcvr) override {
        std::cout << "RCV: on_receiver_error(): " << rcvr.error().what() << std::endl;
    }
};

int main(int argc, char **argv) {
    std::cout << "receiver-handle-link-err" << std::endl;
    if (argc < 3 || argc > 4) {
        std::cerr << "Usage: <connection-url>  <address> [<num-msgs>] [<err-interval>]\n";
        return 1;
    }

    receive_handler handler {};
    handler.conn_url_ = argv[1];
    handler.address_ = argv[2];

    try {
        if (argc >= 4) {
            handler.expected_ = std::stoi(argv[3]);
        }

        proton::container cont {handler};
        cont.run();
    } catch (const std::exception& e) {
        std::cerr << "RCV: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
