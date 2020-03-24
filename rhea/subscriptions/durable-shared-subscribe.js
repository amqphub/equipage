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
    console.error("Usage: durable-shared-subscribe.js <connection-url> <address> [<message-count>]");
    process.exit(1);
}

var conn_url = url.parse(process.argv[2]);
var address = process.argv[3];
var desired = 0;
var received = 0;

if (process.argv.length === 5) {
    desired = parseInt(process.argv[4]);
}

// Set the container ID to a stable value, such as "client-1"
var container = rhea.create_container({id: "client-1"});

container.on("receiver_open", function (event) {
    console.log("SUBSCRIBE: Opened receiver for source address '" +
                event.receiver.source.address + "'");
});

container.on("message", function (event) {
    var message = event.message;

    console.log("SUBSCRIBE: Received message '" + message.body + "'");

    received++;

    if (received == desired) {
        // Detaching the receiver instead of closing it leaves the
        // subscription intact
        event.receiver.detach();

        event.connection.close();
    }
});

var conn_opts = {
    host: conn_url.hostname,
    port: conn_url.port || 5672
};

var conn = container.connect(conn_opts);

// Configure the receiver source for durability
var receiver_opts = {
    source: {
        address: address,
        // Set the receiver name to a stable value, such as "sub-1"
        name: "sub-1",
        // Preserve unsettled delivery state
        durable: 2,
        // Don't expire the source
        expiry_policy: "never",
        // Global means shared across clients (distinct container IDs)
        capabilities: ["shared", "global"]
    }
}

conn.open_receiver(receiver_opts);
