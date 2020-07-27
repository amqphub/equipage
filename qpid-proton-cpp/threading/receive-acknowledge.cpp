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
#include <proton/delivery.hpp>
#include <proton/message.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/receiver.hpp>
#include <proton/receiver_options.hpp>
#include <proton/source.hpp>
#include <proton/work_queue.hpp>

#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <tuple>
#include <vector>

// Prevent garbled logging
std::mutex out_lock_;
#define OUT(x) do { std::lock_guard<std::mutex> l(out_lock_); x; } while (false)

struct worker_message {
    // Provide ongoing (limited) access to Proton objects used outside
    // of a callback.  It is deliberately non-copyable to help prevent
    // thread-safety problems.

    // Construct in on_message() callback.  Destruct in delivery
    // work_queue or a callback of the delivery's connection.

    // delivery_ptr_ points to a Proton reference-counted accessor to
    // an internal Proton object.  The application cannot use mutexes
    // to guaranty thread-safe use of or copying of delivery_ptr_
    // while the engine is running.  Do not access the underlying
    // delivery except when processing a callback from the connection
    // or as work on its work_queue.

    // message_ptr_ points to the inbound message data (move
    // semantics).  The application can use it in any thread with
    // appropriate mutex use.

    std::unique_ptr<proton::delivery> delivery_ptr_;
    std::shared_ptr<proton::message> message_ptr_;

    // Call from on_message() callback
    worker_message(proton::delivery& dlv, proton::message& msg)
        : delivery_ptr_(new proton::delivery {dlv}), message_ptr_(new proton::message {}) {
        swap(*message_ptr_, msg);
    }

    // Only call from the connection's work_queue or one of its
    // callbacks
    ~worker_message() {}

    proton::delivery* delivery() {
        return delivery_ptr_.get();
    }

    proton::message* message() {
        return message_ptr_.get();
    }
};

class receive_handler : public proton::messaging_handler {
    const std::string conn_url_ {};
    const std::string address_ {};

    // Used only in the Proton handler thread
    proton::receiver receiver_ {};

    // Shared by the Proton handler and user threads
    std::mutex lock_ {};
    proton::work_queue* work_queue_ {0};
    std::condition_variable receiver_open_cv_ {};
    std::condition_variable messages_ready_cv_ {};
    std::queue<worker_message*> messages_ {};

    int count_ {0};

public:
    receive_handler(const std::string& conn_url, const std::string& address)
        : conn_url_(conn_url), address_(address) {}

    worker_message* receive() {
        std::unique_lock<std::mutex> l {lock_};
        while (messages_.empty()) messages_ready_cv_.wait(l);

        auto wm = messages_.front();
        messages_.pop();

        return wm;
    }

    void process_message(proton::message& msg) {
        std::unique_lock<std::mutex> l {lock_};

        if (count_++ % 4 == 0) {
            throw std::exception {};
        }
    }

    void accept(proton::delivery* dlv) {
        std::unique_lock<std::mutex> l {lock_};

        work_queue(l)->add([=]() {
            dlv->accept();
        });
    }

    void reject(proton::delivery* dlv) {
        std::unique_lock<std::mutex> l {lock_};

        work_queue(l)->add([=]() {
            dlv->reject();
        });
    }

    void close() {
        std::unique_lock<std::mutex> l {lock_};

        work_queue(l)->add([this]() {
            receiver_.connection().close();
        });
    }

private:
    proton::work_queue* work_queue(std::unique_lock<std::mutex>& l) {
        while (!work_queue_) receiver_open_cv_.wait(l);
        return work_queue_;
    }

    void on_container_start(proton::container& cont) override {
        proton::connection conn = cont.connect(conn_url_);

        proton::receiver_options opts {};
        opts.auto_accept(false);

        conn.open_receiver(address_, opts);
    }

    void on_receiver_open(proton::receiver& rcv) override {
        OUT(std::cout << "RECEIVE: Opened receiver for source address '"
                      << rcv.source().address() << "'\n");

        std::lock_guard<std::mutex> l {lock_};

        receiver_ = rcv;
        work_queue_ = &rcv.work_queue();

        receiver_open_cv_.notify_all();
    }

    void on_message(proton::delivery& dlv, proton::message& msg) override {
        std::lock_guard<std::mutex> l {lock_};

        worker_message *wm = new worker_message {dlv, msg};

        // Note: The proton::message is now empty.  Its contents are
        // now in the worker_message.

        messages_.push(wm);
        messages_ready_cv_.notify_all();
    }

    void on_error(const proton::error_condition& e) override {
        OUT(std::cerr << "RECEIVE: Unexpected error: " << e << "\n");
        exit(1);
    }
};

int main(int argc, const char** argv) {
    if (argc != 3 && argc != 4) {
        std::cerr << "Usage: receive <connection-url> <address> [<message-count>]\n";
        return 1;
    }

    auto conn_url = argv[1];
    auto address = argv[2];
    auto desired = 1;

    if (argc == 4) {
        desired = std::stoi(argv[3]);
    }

    receive_handler handler {conn_url, address};
    proton::container container {handler};

    try {
        std::thread io([&]() {
                container.run();
            });

        std::thread receiver([&]() {
                for (int i = 0; i < desired; ++i) {
                    auto wm = handler.receive();
                    proton::delivery* dlv = wm->delivery();
                    proton::message* msg = wm->message();

                    OUT(std::cout << "RECEIVE: Received message '" << msg->body() << "'\n");

                    try {
                        handler.process_message(*msg);
                        handler.accept(dlv);

                        OUT(std::cout << "RECEIVE: Message accepted\n");
                    } catch (std::exception& e) {
                        handler.reject(dlv);

                        OUT(std::cout << "RECEIVE: Message rejected\n");
                    }
                }

                handler.close();

                OUT(std::cout << "RECEIVE: Closed\n");
            });

        receiver.join();
        io.join();
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }

    return 0;
}
