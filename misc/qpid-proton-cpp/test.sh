#!/usr/bin/bash

set -e

make

server=amqp.zone
address=jobs

./respond $server $address respond.cpp-0 &
respond_pid=$!

trap "kill $respond_pid" EXIT

./request $server $address abc

kill $respond_pid

server=messaging-enmasse.34.210.100.115.nip.io:443
address=test1

./respond $server $address respond.cpp-0 1 &
respond_pid=$!

trap "kill $respond_pid" EXIT

./request $server $address abc 1
