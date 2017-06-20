#!/usr/bin/bash

set -e

server=amqp.zone
address=jobs

python respond.py $server $address respond.py-0 &
respond_pid=$!

trap "kill $respond_pid" EXIT

python request.py $server $address abc
