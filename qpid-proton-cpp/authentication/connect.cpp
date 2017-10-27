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

#include <iostream>

struct handler : public proton::messaging_handler {
    void on_connection_open(proton::connection& conn) override {
        std::cout << "Connected!" << std::endl;
        conn.close();
    }
};

int main(int argc, char** argv) {
    std::string authority = argv[1];

    handler h;
    proton::container container(h);

    proton::connection_options opts;
    opts.sasl_allowed_mechs("GSSAPI");

    container.connect(authority, opts);
    container.run();

    return 0;
}
