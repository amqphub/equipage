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

var container = rhea.create_container();

container.on("connection_open", function (context) {
    console.log("Connected!");
});

var conn_url = url.parse(process.argv[2]); // XXX Not being used anywhere
var conn_opts = {};

// An initial delay of 10 milliseconds, backing off to a max delay of
// 1 second.  Stop after 10 reconnect attempts.

conn_opts.initial_reconnect_delay = 10;
conn_opts.max_reconnect_delay = 1000;
conn_opts.reconnect_limit = 10;

container.connect(conn_opts);
