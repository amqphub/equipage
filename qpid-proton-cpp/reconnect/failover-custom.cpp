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
#include <proton/messaging_handler.hpp>
#include <proton/transport.hpp>
#include <proton/work_queue.hpp>

#include <iostream>
#include <string>

struct handler : public proton::messaging_handler {
    std::vector<std::string> servers;
    int current_server_index;

    handler(std::vector<std::string> s) : servers(s), current_server_index(0) {}

    std::string current_server() {
        return servers[current_server_index];
    }

    void connect(proton::container& cont) {
        std::cout << "Connecting to " << current_server() << std::endl;

        cont.connect(current_server());
    }

    void on_container_start(proton::container& cont) {
        connect(cont);
    }

    void on_connection_open(proton::connection& conn) {
        std::cout << "Connected to " << current_server() << std::endl;
    }

    void on_transport_error(proton::transport& trans) {
        std::cout << "Disconnected from " << current_server() << std::endl;

        current_server_index += 1;

        if (current_server_index == servers.size()) {
            current_server_index = 0;
        }

        proton::container& cont = trans.connection().container();

        cont.schedule(proton::duration(1000), [&]() { this->connect(cont); });
    }
};

int main(int argc, char** argv) {
    std::vector<std::string> servers(argv + 1, argv + argc);

    handler h(servers);
    proton::container cont(h);

    cont.run();

    return 0;
}
