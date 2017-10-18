#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import argparse
import sys

from plano import *

def open_test_session(session):
    set_message_threshold("error")

def test_qpid_proton_cpp_connect(session):
    with TestServer() as server:
        call("qpid-proton-cpp/build/connect {}", server.connection_url)

def test_qpid_proton_python_connect(session):
    with TestServer() as server:
        call("qpid-proton-python/connect.py {}", server.connection_url)

def test_rhea_connect(session):
    with TestServer() as server:
        call("rhea/connect.js {}", server.connection_url)

class TestServer(object):
    def __init__(self):
        port = random_port()

        self.proc = start_process("qbroker --quiet --port {}", port)
        self.proc.connection_url = "//127.0.0.1:{}".format(port)

    def __enter__(self):
        return self.proc

    def __exit__(self, exc_type, exc_value, traceback):
        stop_process(self.proc)

# def start_qmessage(args, **kwargs):
#     return start_process("qmessage --verbose {}", args, **kwargs)

# def start_qsend(url, args, **kwargs):
#     return start_process("qsend --verbose {} {}", url, args, **kwargs)

# def start_qreceive(url, args, **kwargs):
#     return start_process("qreceive --verbose {} {}", url, args, **kwargs)

# def start_qrequest(url, args, **kwargs):
#     return start_process("qrequest --verbose {} {}", url, args, **kwargs)

# def start_qrespond(url, args, **kwargs):
#     return start_process("qrespond --verbose {} {}", url, args, **kwargs)

# def send_and_receive(url, qmessage_args="", qsend_args="", qreceive_args="--count 1"):
#     message_proc = start_qmessage(qmessage_args, stdout=PIPE)
#     send_proc = start_qsend(url, qsend_args, stdin=message_proc.stdout)
#     receive_proc = start_qreceive(url, qreceive_args, stdout=PIPE)

#     try:
#         check_process(message_proc)
#         check_process(send_proc)
#         check_process(receive_proc)
#     except CalledProcessError:
#         terminate_process(message_proc)
#         terminate_process(send_proc)
#         terminate_process(receive_proc)

#         raise

#     output = receive_proc.communicate()[0].decode()

#     return output[:-1]

# def request_and_respond(url, qmessage_args="", qrequest_args="", qrespond_args="--count 1"):
#     message_proc = start_qmessage(qmessage_args, stdout=PIPE)
#     request_proc = start_qrequest(url, qrequest_args, stdin=message_proc.stdout, stdout=PIPE)
#     respond_proc = start_qrespond(url, qrespond_args)

#     try:
#         check_process(message_proc)
#         check_process(request_proc)
#         check_process(respond_proc)
#     except CalledProcessError:
#         terminate_process(message_proc)
#         terminate_process(request_proc)
#         terminate_process(respond_proc)

#         raise

#     output = request_proc.communicate()[0].decode()

#     return output[:-1]

# def test_send_receive(session):
#     with TestServer() as server:
#         body = send_and_receive(server.url, "--body abc123", "", "--count 1 --no-prefix")
#         assert body == "abc123", body

#         send_and_receive(server.url, "", "--presettled")
#         send_and_receive(server.url, "", "-m abc --message xyz", "--count 2")
#         send_and_receive(server.url, "--count 10", "", "--count 10")
#         send_and_receive(server.url, "--count 10 --rate 1000", "", "--count 10")

# def test_request_respond(session):
#     with TestServer() as server:
#         body = request_and_respond(server.url, "--body abc123", "--no-prefix", "--count 1 --reverse --upper --append ' and this'")
#         assert body == "321CBA and this", body

#         request_and_respond(server.url, "", "--presettled")
#         request_and_respond(server.url, "", "-m abc --message xyz", "--count 2")
#         request_and_respond(server.url, "--count 10", "", "--count 10")
#         request_and_respond(server.url, "--count 10 --rate 1000", "", "--count 10")

# def test_message(session):
#     with TestServer() as server:
#         send_and_receive(server.url, "--id m1 --correlation-id c1")
#         send_and_receive(server.url, "--user ssorj")
#         send_and_receive(server.url, "--to xyz --reply-to abc")
#         send_and_receive(server.url, "--durable")
#         send_and_receive(server.url, "--priority 100")
#         send_and_receive(server.url, "--ttl 100.1")
#         send_and_receive(server.url, "--body hello")
#         send_and_receive(server.url, "--property x y --property a b")
