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
            std::cout << "listening on " << l.port() << std::endl;
        }
    };

    std::string url;
    proton::listener listener;
    listener_ready_handler listen_handler;
    int expected;
    int received;
    int err_interval;

  public:
    direct_recv(const std::string &s, int c, int ei) :
        url(s), expected(c), received(0), err_interval(ei) {}

    void on_container_start(proton::container &c) override {
        listener = c.listen(url, listen_handler);
    }

    void on_message(proton::delivery &d, proton::message &msg) override {
        if (proton::coerce<int>(msg.id()) < received) {
            return; // Ignore duplicate
        }

        if (expected == 0 || received < expected) {
            std::cout << msg.body();
            received++;

            // Simulate a link failure with error every err_interval messages
            if (received%err_interval == 0) {
                std::cout << " - closing receiver with error";
                d.receiver().close(proton::error_condition("Test close"));
            }
            std::cout << std::endl;
        }

        if (received == expected) {
            d.receiver().close();
            d.connection().close();
            listener.stop();
        }
    }

    void on_receiver_open(proton::receiver &r) override {
        std::cout << "receiver opened" << std::endl;
        proton::messaging_handler::on_receiver_open(r);
    }
};

int main(int argc, char **argv) {
    direct_recv recv("127.0.0.1:5672/examples", 250, 30);
    proton::container(recv).run();
}
