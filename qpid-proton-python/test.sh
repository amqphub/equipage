#!/usr/bin/bash

set -e

server=amqp.zone
address=jobs

python respond.py $server $address respond.py-0 &
respond_pid=$!

trap "kill $respond_pid" EXIT

python request.py $server $address abc

kill $respond_pid

server=messaging-enmasse.34.210.100.115.nip.io:443
address=myqueue

python respond.py $server $address respond.py-0 1 &
respond_pid=$!

trap "kill $respond_pid" EXIT

python request.py $server $address abc 1
