#!/usr/bin/env node

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

var conn_url = url.parse(process.argv[2]);
var address = process.argv[3];
var count = parseInt(process.argv[4]);

var received = 0;
var stopping = false;

var container = rhea.create_container();

container.on("connection_open", function (event) {
    console.log("RECEIVE: Connected to '" + conn_url + "'");
});

container.on("receiver_open", function (event) {
    console.log("RECEIVE: Opened receiver for source address '" + address + "'");
});

container.on("message", function (event) {
    if (stopping) return;

    var message = event.message;
    
    console.log("RECEIVE: Received message '" + message.body + "'");

    received++;

    if (received == count) {
        event.connection.close();
        stopping = true;
    }
});

var opts = {
    "host": conn_url.hostname,
    "port": conn_url.port || 5672
};

var conn = container.connect(opts);
conn.open_receiver(address);
