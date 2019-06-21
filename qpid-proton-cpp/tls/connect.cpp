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
#include <proton/ssl.hpp>

#include <iostream>
#include <string>

struct connect_handler : public proton::messaging_handler {
    std::string conn_url_;

    void on_container_start(proton::container& cont) override {
        std::cout << "CONNECT: Connecting to '" << conn_url_ << "'\n";

        proton::ssl_client_options sopts {"/etc/pki/ca-trust"};
        proton::connection_options opts {};

        opts.ssl_client_options(sopts);

        cont.connect(conn_url_, opts);
    }

    void on_connection_open(proton::connection& conn) override {
        std::cout << "CONNECT: Connected to '" << conn_url_ << "'\n";
        conn.close();
    }
};

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "Usage: connect <connection-url>\n";
        return 1;
    }

    connect_handler handler {};
    handler.conn_url_ = argv[1];

    proton::container cont {handler};

    try {
        cont.run();
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }

    return 0;
}
