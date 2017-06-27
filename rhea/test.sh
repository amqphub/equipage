#!/usr/bin/bash

set -ex

npm install

server=amqp.zone
address=jobs

node respond.js $server $address respond.js-0 &
respond_pid=$!

trap "kill $respond_pid" EXIT

node request.js $server $address abc

kill $respond_pid

server=messaging-enmasse.34.210.100.115.nip.io:443
address=test1

node respond.js $server $address respond.js-0 1 &
respond_pid=$!

trap "kill $respond_pid" EXIT

node request.js $server $address abc 1

kill $respond_pid
