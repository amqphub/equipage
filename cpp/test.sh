#!/usr/bin/bash

set -e

host=amqp.zone
port=5672
address=jobs

make

./respond $host $port $address respond.cpp-0 &
processor_pid=$!

trap "kill $processor_pid" EXIT

./request $host $port $address abc
