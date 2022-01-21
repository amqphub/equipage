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


class direct_recv : public proton::messaging_handler {
  private:
    class listener_ready_handler : public proton::listen_handler {
        void on_open(proton::listener& l) override {
            std::cout << "listen_handler::on_open: listening on " << l.port() << std::endl;
        }
    };

    std::string url;
    proton::listener listener;
    listener_ready_handler listen_handler;
    int expected;
    int received;

  public:
    direct_recv(const std::string &s, int c) : url(s), expected(c), received(0) {}

    void on_container_start(proton::container &c) override {
        std::cout << "on_container_start" << std::endl;
        listener = c.listen(url, listen_handler);
    }

    void on_message(proton::delivery &d, proton::message &msg) override {
        if (proton::coerce<int>(msg.id()) < received) {
            return; // Ignore duplicate
        }

        if (expected == 0 || received < expected) {
            std::cout << "on_message: " << msg.body() << std::endl;
            received++;
        }

        if (received == expected) {
            d.receiver().close();
            d.connection().close();
            listener.stop();
        }
    }

    // Override on_receiver_error() so that default handler method is not used.
    // When the sender re-opens, the listener will automatically re-open.
    void on_receiver_error(proton::receiver &r) override {
        std::cout << "on_receiver_error: " << r.error().what() << std::endl;
    }
};

int main(int argc, char **argv) {
        direct_recv recv("127.0.0.1:5672/examples", 250);
        proton::container(recv).run();
}
