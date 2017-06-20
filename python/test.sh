#!/usr/bin/bash

set -e

host=amqp.zone
port=5672
address=jobs

python respond.py $host $port $address respond.py-0 &
processor_pid=$!

trap "kill $processor_pid" EXIT

python request.py $host $port $address abc
