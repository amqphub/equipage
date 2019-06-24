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
#include <proton/receiver_options.hpp>
#include <proton/receiver.hpp>
#include <proton/sender.hpp>
#include <proton/source_options.hpp>
#include <proton/target.hpp>
#include <proton/uuid.hpp>

#include <iostream>
#include <string>

struct request_handler : public proton::messaging_handler {
    std::string conn_url_ {};
    std::string address_ {};
    std::string message_body_ {};
    proton::sender sender_ {};

    void on_container_start(proton::container& cont) override {
        proton::connection conn = cont.connect(conn_url_);

        sender_ = conn.open_sender(address_);

        proton::receiver_options opts {};
        proton::source_options sopts {};

        sopts.dynamic(true);
        opts.source(sopts);

        conn.open_receiver("", opts);
    }

    void on_sender_open(proton::sender& snd) override {
        std::cout << "REQUEST: Opened sender for target address '"
                  << snd.target().address() << "'\n";
    }

    void on_receiver_open(proton::receiver& rcv) override {
        std::cout << "REQUEST: Opened dynamic receiver for responses\n";

        proton::message request {message_body_};
        request.id(proton::message_id {proton::uuid::random()});
        request.reply_to(rcv.source().address());

        sender_.send(request);

        std::cout << "REQUEST: Sent request '" << request.body() << "'\n";
    }

    void on_message(proton::delivery& dlv, proton::message& response) override {
        std::cout << "REQUEST: Received response '" << response.body() << "'\n";

        dlv.receiver().close();
        dlv.connection().close();
    }
};

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "Usage: request <connection-url> <address> <message-body>\n";
        return 1;
    }

    request_handler handler {};
    handler.conn_url_ = argv[1];
    handler.address_ = argv[2];
    handler.message_body_ = argv[3];

    proton::container cont {handler};

    try {
        cont.run();
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }

    return 0;
}
