#!/usr/bin/bash

set -e

host=127.0.0.1
port=56720
address=jobs

qbroker --host $host --port $port &
broker_pid=$!

sleep 1

node processor.js $host $port $address p1 &
processor_pid=$!

trap "kill $broker_pid $processor_pid" EXIT

node request.js $host $port $address abc
