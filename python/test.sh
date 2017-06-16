#!/usr/bin/bash

set -e

host=amqp.zone
port=5672
address=jobs

python processor.py $host $port $address p1 &
processor_pid=$!

trap "kill $processor_pid" EXIT

python request.py $host $port $address abc
