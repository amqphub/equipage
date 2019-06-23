/*
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
 */

#include <proton/connection.hpp>
#include <proton/container.hpp>
#include <proton/message.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/connection_options.hpp>
#include <proton/sender.hpp>
#include <proton/work_queue.hpp>

#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>

class client : public proton::messaging_handler {
    std::string conn_url_;
    std::string addr_;

    proton::sender sender_;
    std::queue<proton::message> messages_;

    std::mutex mutex_;
    std::condition_variable sender_ready_;
    std::condition_variable messages_ready_;

  public:
    client(const std::string& conn_url, const std::string& addr) :
        conn_url_(conn_url), addr_(addr) {}

    void send(const proton::message& msg) {
        std::unique_lock<std::mutex> l(mutex_);
        if (!sender_) sender_ready_.wait(l);

        sender_.work_queue().add([=]() { sender_.send(msg); });
    }

    proton::message receive() {
        std::unique_lock<std::mutex> l(mutex_);
        while (messages_.empty()) messages_ready_.wait(l);

        auto msg = std::move(messages_.front());
        messages_.pop();

        return msg;
    }

    void close() {
        std::unique_lock<std::mutex> l(mutex_);
        if (!sender_) sender_ready_.wait(l);

        sender_.connection().work_queue().add([this]() { sender_.connection().close(); });
    }

  private:
    // XXX Move work queue access here
    
    void on_container_start(proton::container& cont) override {
        cont.connect(conn_url_);
    }

    void on_connection_open(proton::connection& conn) override {
        conn.open_sender(addr_);
        conn.open_receiver(addr_);
    }

    void on_sender_open(proton::sender& snd) override {
        std::lock_guard<std::mutex> l(mutex_);
        sender_ = snd;
        sender_ready_.notify_all();
    }

    void on_message(proton::delivery& dlv, proton::message& msg) override {
        std::lock_guard<std::mutex> l(mutex_);
        messages_.push(msg);
        messages_ready_.notify_all();
    }
};

int main(int argc, const char** argv) {
    try {
        if (argc != 4) {
            std::cerr
                << "Usage: client <connection-url> <address> <message-count>" << std::endl
                << "  <connection-url>: amqp://127.0.0.1" << std::endl
                << "  <address>: q0" << std::endl
                << "  <message-count>: 10" << std::endl;
            return 1;
        }

        auto url = argv[1];
        auto address = argv[2];
        auto count = atoi(argv[3]);

        client client_(url, address);
        proton::container container(client_);

        std::thread io([&]() { container.run(); });

        std::thread sender([&]() {
                for (int i = 0; i < count; ++i) {
                    proton::message msg(std::to_string(i + 1));
                    client_.send(msg);
                    std::cout << "Sent message " << msg.body() << std::endl;
                }
            });

        std::thread receiver([&]() {
                for (int i = 0; i < count; ++i) {
                    auto msg = client_.receive();
                    std::cout << "Received message " << msg.body() << std::endl;
                }

                client_.close();
            });

        sender.join();
        receiver.join();
        io.join();

        return 0;
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }

    return 1;
}
