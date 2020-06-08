#!/usr/bin/node

//
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.
//

"use strict";

var rhea = require("rhea");
var url = require("url");

if (process.argv.length !== 4 && process.argv.length !== 5) {
    console.error("Usage: receive.js <connection-url> <address> [<message-count>]");
    process.exit(1);
}

var listen_url = url.parse(process.argv[2]);
var address = process.argv[3];
var desired = 0;
var received = 0;

if (process.argv.length === 5) {
    desired = parseInt(process.argv[4]);
}

var container = rhea.create_container();
var server;

container.on("receiver_open", function (event) {
    console.log("RECEIVE: Opened receiver for target address '" +
                event.receiver.remote.attach.target.address + "'");

    // Set the target address using the value from the remote peer
    address = event.receiver.remote.attach.target.address;
    event.receiver.set_target({address: address});
});

container.on("message", function (event) {
    console.log("RECEIVE: Received message '" + event.message.body + "'");

    received++;

    if (received == desired) {
        event.receiver.close();
        event.connection.close();
        server.close();
    }
});

var opts = {
    host: listen_url.hostname,
    port: listen_url.port || 5672,
};

server = container.listen(opts);

console.log("RECEIVE: Listening at " + url.format(listen_url));
