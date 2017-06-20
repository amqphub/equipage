#!/usr/bin/bash

set -e

host=amqp.zone
port=5672
address=jobs

node respond.js $host $port $address respond.js-0 &
processor_pid=$!

trap "kill $processor_pid" EXIT

node request.js $host $port $address abc
