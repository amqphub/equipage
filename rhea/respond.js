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

if (process.argv.length !== 4 && process.argv.length !== 5) {
    console.error("Usage: respond.js CONNECTION-URL ADDRESS [MESSAGE-COUNT]");
    process.exit(1);
}

var conn_url = url.parse(process.argv[2]);
var address = process.argv[3];

var desired = 0;
var received = 0;

if (process.argv.length === 5) {
    desired = parseInt(process.argv[4]);
}

var container = rhea.create_container();

container.on("connection_open", function (event) {
    event.connection.open_receiver(address);
});

container.on("message", function (event) {
    var request = event.message;

    console.log("RESPOND: Received request '" + request.body + "'");

    var body = request.body.toUpperCase();
    
    var response = {
        to: request.reply_to,
        correlation_id: request.id, // XXX
        body: body,
    };

    event.connection.send(response);

    console.log("RESPOND: Sent response '" + response.body + "'");
});

var opts = {
    host: conn_url.hostname,
    port: conn_url.port || 5672
};

container.connect(opts);
