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
#include <proton/message.hpp>
#include <proton/messaging_handler.hpp>
#include <proton/tracker.hpp>
#include <proton/types.hpp>

#include <iostream>
#include <map>


class simple_send : public proton::messaging_handler {
  private:
    std::string url;
    bool reconnect;
    proton::sender sender;
    int sent;
    int confirmed;
    int total;

  public:
    simple_send(const std::string &s, int c) :
        url(s), sent(0), confirmed(0), total(c) {}

    void on_container_start(proton::container &c) override {
        sender = c.open_sender(url);
    }

    void on_connection_open(proton::connection& c) override {
        if (c.reconnected()) {
            sent = confirmed;   // Re-send unconfirmed messages after a reconnect
        }
    }

    void on_sendable(proton::sender &s) override {
        if (s.credit() && sent < total) {
            proton::message msg;
            std::map<std::string, int> m;
            m["sequence"] = sent + 1;

            msg.id(sent + 1);
            msg.body(m);

            s.send(msg);
            sent++;
            std::cout << "sent=" << sent << std::endl;
        }
    }

    // Override on_sender_close to re-open if the expected number of messages
    // have not been received. Reset sent count in case some messages were lost.
    void on_sender_close(proton::sender &s) override {
        std::cout << "on_sender_close";
        if (confirmed != total) {
            s.connection().open_sender(url);
            sent = confirmed;   // Re-send unconfirmed messages after a reconnect
            std::cout << " - reopening sender, sent reset to " << sent;
        }
        std::cout << std::endl;
    }

    // Override on_sender_error() so that default handler method is not used.
    void on_sender_error(proton::sender &s) override {
        std::cout << "on_sender_error: " << s.error().what() << std::endl;
    }

    void on_tracker_accept(proton::tracker &t) override {
        confirmed++;

        std::cout << "confirmed=" << confirmed << std::endl;
        if (confirmed == total) {
            std::cout << "all messages confirmed" << std::endl;
            t.connection().close();
        }
    }

    void on_transport_close(proton::transport &) override {
        sent = confirmed;
    }
};

int main(int argc, char **argv) {
    simple_send send("127.0.0.1:5672/examples", 250);
    proton::container(send).run();
}
