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

#include <proton/default_container.hpp>

#include <proton/connection.hpp>
#include <proton/connection_options.hpp>
#include <proton/container.hpp>
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
    std::string connection_url;
    std::string address;
    std::string message_body;
    bool sent;

    void on_container_start(proton::container& cont) override {
        proton::connection_options opts;
        opts.sasl_allowed_mechs("ANONYMOUS");

        proton::connection conn = cont.connect(connection_url, opts);
        conn.open_sender(address);

        // print("SENDER: Created sender for target address '{0}'".format(self.address))
    }

    void on_sendable(proton::sender& snd) override {
        if (sent) return;

        proton::message msg = proton::message(message_body);

        snd.send(msg);

        // print("SENDER: Sent message '{0}'".format(self.message_body))
        //std::cout << "request.cpp: Sent request '" << request.body() << "'" << std::endl;

        snd.connection().close();

        sent = true;
    }
};

int main(int argc, char** argv) {
    std::string connection_url = argv[1];

    handler h;
    h.address = argv[2];
    h.message_body = argv[3];

    proton::container container(h);

    container.run();

    return 0;
}
