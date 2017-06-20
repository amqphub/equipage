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
var data = process.argv[4];

var container = rhea.create_container();
var sender = null;

container.on("connection_open", function (context) {
    sender = context.connection.open_sender(address);
    context.connection.open_receiver({source: {dynamic: true}});
});

container.on("receiver_open", function (context) {
    var request = {
        reply_to: context.receiver.source.address,
        body: data
    };
    
    sender.send(request);

    console.log("request.js: Sent request '" + request.body + "'");
});

container.on("message", function (context) {
    console.log("request.js: Received response '" + context.message.body + "'");

    context.connection.close();
});

var [host, port] = server.split(":", 2);

container.connect({username: "anonymous", host: host, port: port});
