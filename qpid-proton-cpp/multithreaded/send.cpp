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

//
// C++11 or greater
//
// A multi-threaded client that calls proton::container::run() in one
// thread and sends messages in another.
//

#include <proton/connection.hpp>
#include <proton/connection_options.hpp>
#include <proton/container.hpp>
#include <proton/message.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/sender.hpp>
#include <proton/work_queue.hpp>

#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <sstream>
#include <string>
#include <thread>

// Prevent garbled logging
std::mutex out_lock_;
#define OUT(x) do { std::lock_guard<std::mutex> l(out_lock_); x; } while (false)

// Handler for a single thread-safe sending connection
class send_handler : public proton::messaging_handler {
    const std::string conn_url_;
    const std::string address_;
    const int max_outgoing_bytes_ {20};

    // Used only in the proton handler thread
    proton::sender sender_;

    // Shared by the proton handler and user threads
    std::mutex lock_;
    proton::work_queue* work_queue_ {0};
    std::condition_variable sender_open_cv_;
    bool sender_has_capacity_;
    std::condition_variable sender_has_capacity_cv_;

public:
    send_handler(const std::string& conn_url, const std::string& address)
        : conn_url_(conn_url), address_(address) {}

    // Thread safe
    void send(const proton::message& msg) {
        std::unique_lock<std::mutex> l(lock_);
        while (!sender_has_capacity_) sender_has_capacity_cv_.wait(l);
        sender_has_capacity_ = false;

        work_queue(l)->add([=]() { sender_.send(msg); });
    }

    // Thread safe
    void close() {
        std::unique_lock<std::mutex> l(lock_);
        work_queue(l)->add([=]() { sender_.connection().close(); });
    }

private:
    proton::work_queue* work_queue(std::unique_lock<std::mutex>& l) {
        while (!work_queue_) sender_open_cv_.wait(l);
        return work_queue_;
    }

    void on_container_start(proton::container& cont) override {
        cont.connect(conn_url_);
    }

    void on_connection_open(proton::connection& conn) override {
        conn.open_sender(address_);
    }

    void on_sender_open(proton::sender& snd) override {
        std::lock_guard<std::mutex> l(lock_);

        sender_ = snd;
        work_queue_ = &snd.work_queue();

        sender_open_cv_.notify_all();
    }

    void on_sendable(proton::sender& snd) override {
        std::lock_guard<std::mutex> l(lock_);

        if (snd.session().outgoing_bytes() < max_outgoing_bytes_) {
            sender_has_capacity_ = true;
            sender_has_capacity_cv_.notify_all();
        } else {
            OUT(std::cout << "Max bytes exceeded.  Blocking sends.\n");
        }
    }

    void on_error(const proton::error_condition& e) override {
        OUT(std::cerr << "Unexpected error: " << e << "\n");
        exit(1);
    }
};

int main(int argc, const char** argv) {
    if (argc != 4) {
        std::cerr << "Usage: send CONNECTION-URL ADDRESS MESSAGE-COUNT\n";
        return 1;
    }

    auto conn_url = argv[1];
    auto address = argv[2];
    auto count = atoi(argv[3]);

    send_handler handler(conn_url, address);
    proton::container container(handler);

    try {
        std::thread io([&]() { container.run(); });

        std::thread sender([&]() {
                for (int i = 0; i < count; ++i) {
                    proton::message msg(std::to_string(i + 1));
                    handler.send(msg);
                    OUT(std::cout << "Sent message " << msg.body() << "\n");
                }

                handler.close();
            });

        sender.join();
        io.join();
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }

    return 0;
}
