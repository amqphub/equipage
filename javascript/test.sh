#!/usr/bin/bash

set -e

host=amqp.zone
port=5672
address=jobs

node processor.js $host $port $address p1 &
processor_pid=$!

trap "kill $processor_pid" EXIT

node request.js $host $port $address abc
