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
#include <proton/reconnect_options.hpp>
#include <proton/transport.hpp>

#include <iostream>
#include <string>

struct handler : public proton::messaging_handler {
    std::string primary_server;
    std::vector<std::string> failover_servers;

    handler(std::string p, std::vector<std::string> f) : primary_server(p), failover_servers(f) {}

    void on_container_start(proton::container& cont) {
        proton::reconnect_options ro;
        proton::connection_options co;

        ro.failover_urls(failover_servers);
        co.reconnect(ro);

        cont.connect(primary_server, co);
    }

    void on_connection_open(proton::connection& conn) {
        std::cout << "Connected to " << conn.transport() << std::endl;
    }
};

int main(int argc, char** argv) {
    std::string primary_server = argv[1];
    std::vector<std::string> failover_servers(&argv[2], &argv[argc]);

    std::cout << primary_server << std::endl;

    for (int i = 0; i < failover_servers.size(); i++) {
        std::cout << failover_servers.at(i) << std::endl;
    }

    handler h(primary_server, failover_servers);

    proton::container(h).run();

    return 0;
}
