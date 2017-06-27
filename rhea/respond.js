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

var server = process.argv[2];
var address = process.argv[3];
var id = process.argv[4];
var tls_enabled = false;

if (process.argv.length === 6) {
    tls_enabled = process.argv[5] === 1;
}

var container = rhea.create_container({id: id});

container.on("connection_open", function (context) {
    context.connection.open_receiver(address);
});

container.on("message", function (context) {
    var request = context.message;

    console.log(container.id + ": Received request '" + request.body + "'");

    var body = request.body.toUpperCase() + " [" + container.id + "]";
    
    var response = {
        to: request.reply_to,
        body: body,
        correlation_id: request.correlation_id
    };

    context.connection.send(response);

    console.log(container.id + ": Sent response '" + response.body + "'");
});

var [host, port] = server.split(":", 2);
var opts = {};

opts.username = "anonymous";
opts.host = host;
opts.port = port;

if (tls_enabled) {
    opts.transport = "tls";
    opts.servername = host;
    opts.rejectUnauthorized = false;
}

container.connect(opts);
