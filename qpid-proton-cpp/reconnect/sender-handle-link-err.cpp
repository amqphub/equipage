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
#include <proton/tracker.hpp>
#include <proton/types.hpp>

#include <iostream>
#include <map>


struct send_handler : public proton::messaging_handler {
    std::string conn_url_ {};
    std::string address_ {};
    int total_ {250};
    proton::sender sender_ {};
    int sent_ {0};
    int confirmed_ {0};

    void on_container_start(proton::container &cont) override {
        sender_ = cont.open_sender(conn_url_ + "/" + address_);
    }

    void on_connection_open(proton::connection& conn) override {
        if (conn.reconnected()) {
            sent_ = confirmed_;   // Re-send unconfirmed messages after a reconnect
        }
        std::cout << "SND: on_connection_open() sent_=" << sent_ << std::endl;
    }

    void on_sendable(proton::sender &sndr) override {
        if (sndr.credit() && sent_ < total_) {
            std::map<std::string, int> msg_body;
            msg_body["sequence"] = sent_ + 1;

            proton::message msg;
            msg.id(sent_ + 1);
            msg.body(msg_body);

            sndr.send(msg);
            sent_++;
            std::cout << "SND: " << msg.body() << std::endl;
        }
    }

    // Override on_sender_close to re-open if the expected number of messages
    // have not been received. Reset sent count in case some messages were lost.
    void on_sender_close(proton::sender &sndr) override {
        std::cout << "SND: on_sender_close()";
        if (confirmed_ != total_) {
            sndr.connection().open_sender(conn_url_ + "/" + address_);
            sent_ = confirmed_;   // Re-send unconfirmed messages after a reconnect
            std::cout << " - reopening sender, sent_ reset to " << sent_;
        }
        std::cout << std::endl;
    }

    // Override on_sender_error() so that default handler method is not used.
    void on_sender_error(proton::sender &sndr) override {
        std::cout << "SND: on_sender_error(): " << sndr.error().what() << std::endl;
    }

    void on_tracker_accept(proton::tracker &trkr) override {
        confirmed_++;

        std::cout << "SND: confirmed " << confirmed_;
        if (confirmed_ == total_) {
            std::cout << " - all messages confirmed";
            trkr.connection().close();
        }
        std::cout << std::endl;
    }

    void on_transport_close(proton::transport &) override {
        sent_ = confirmed_;
    }
};

int main(int argc, char **argv) {
    std::cout << "sender-handle-link-err" << std::endl;
    if (argc < 3 || argc > 4) {
        std::cerr << "Usage: <connection-url>  <address> [<num-msgs>] [<err-interval>]\n";
        return 1;
    }

    send_handler handler {};
    handler.conn_url_ = argv[1];
    handler.address_ = argv[2];

    try {
        if (argc >= 4) {
            handler.total_ = std::stoi(argv[3]);
        }

        proton::container cont {handler};
        cont.run();
    } catch (const std::exception& e) {
        std::cerr << "SND: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
