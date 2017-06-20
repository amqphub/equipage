#!/usr/bin/bash

set -e

server=amqp.zone
address=jobs

make

./respond $server $address respond.cpp-0 &
respond_pid=$!

trap "kill $respond_pid" EXIT

./request $server $address abc
