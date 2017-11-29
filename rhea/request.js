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

if (process.argv.length !== 5) {
    console.error("Usage: request.js CONNECTION-URL ADDRESS MESSAGE-BODY");
    process.exit(1);
}

var conn_url = url.parse(process.argv[2]);
var address = process.argv[3];
var message_body = process.argv[4];

var container = rhea.create_container();
var sender = null;

container.on("connection_open", function (event) {
    sender = event.connection.open_sender(address);
    event.connection.open_receiver({source: {dynamic: true}});
});

container.on("receiver_open", function (event) {
    var request = {
        reply_to: event.receiver.source.address,
        body: message_body
    };
    
    sender.send(request);

    console.log("REQUEST: Sent request '" + request.body + "'");
});

container.on("message", function (event) {
    console.log("REQUEST: Received response '" + event.message.body + "'");

    event.connection.close();
});

var opts = {
    host: conn_url.hostname,
    port: conn_url.port || 5672
};

container.connect(opts);
