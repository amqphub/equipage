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

var conn_urls = process.argv.slice(2);
var conn_opts = {};
var index = -1;

conn_urls = conn_urls.map(url.parse);

// A function in the 'connection_details' property defines connection
// options programatically.  It's called once for each connection
// attempt.  Here we use each new call to connect to an alternate
// server.

conn_opts.connection_details = function() {
    index += 1;

    if (index == conn_urls.length) index = 0;
    
    var opts = {
        "host": conn_urls[index].hostname,
        "port": conn_urls[index].port || 5672
    };

    console.log(opts);
    
    return opts;
};

container.connect(conn_opts);
