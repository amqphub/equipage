#!/usr/bin/bash

set -e

server=amqp.zone
address=jobs

npm install

node respond.js $server $address respond.js-0 &
respond_pid=$!

trap "kill $respond_pid" EXIT

node request.js $server $address abc
