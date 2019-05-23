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

from plano import *

def open_test_session(session):
    enable_logging(level="error")

def test_pooled_jms_connect(session):
    with working_dir("pooled-jms"):
        check_connect_usage(qpid_jms_prog("examples.Connect"))

        with TestServer() as server:
            call("{} {}", qpid_jms_prog("examples.Connect"), server.connection_url)

def test_pooled_jms_configure(session):
    with working_dir("pooled-jms"):
        check_connect_usage(qpid_jms_prog("examples.Configure"))

        with TestServer() as server:
            call("{} {}", qpid_jms_prog("examples.Configure"), server.connection_url)

def test_pooled_jms_makefile(session):
    with working_dir("pooled-jms"):
        with TestServer() as server:
            call("make run URL={}", server.connection_url)

def test_qpid_jms_connect(session):
    with working_dir("qpid-jms"):
        check_connect_usage(qpid_jms_prog("examples.Connect"))

        with TestServer() as server:
            call("{} {}", qpid_jms_prog("examples.Connect"), server.connection_url)

def test_qpid_jms_send_receive(session):
    with working_dir("qpid-jms"):
        check_send_usage(qpid_jms_prog("examples.Send"))
        check_receive_usage(qpid_jms_prog("examples.Receive"))

        with TestServer() as server:
            call("{} {} q1 abc", qpid_jms_prog("examples.Send"), server.connection_url)
            call("{} {} q1 1", qpid_jms_prog("examples.Receive"), server.connection_url)

def test_qpid_jms_request_respond(session):
    #with working_env(PN_TRACE_FRM=1):
    with working_dir("qpid-jms"):
        check_request_usage(qpid_jms_prog("examples.Request"))
        check_respond_usage(qpid_jms_prog("examples.Respond"))

        with TestServer() as server:
            with start_process("{} {} q1 1", qpid_jms_prog("examples.Respond"), server.connection_url):
                sleep(1)
                call("{} {} q1 abc", qpid_jms_prog("examples.Request"), server.connection_url)

def test_qpid_jms_makefile(session):
    with working_dir("qpid-jms"):
        with TestServer() as server:
            call("make run URL={}", server.connection_url)

def test_qpid_proton_cpp_connect(session):
    with working_dir("qpid-proton-cpp"):
        check_connect_usage("build/connect")

        with TestServer() as server:
            call("build/connect {}", server.connection_url)

def test_qpid_proton_cpp_send_receive(session):
    with working_dir("qpid-proton-cpp"):
        check_send_usage("build/send")
        check_receive_usage("build/receive")

        with TestServer() as server:
            call("build/send {} q1 abc", server.connection_url)
            call("build/receive {} q1 1", server.connection_url)

def test_qpid_proton_cpp_request_respond(session):
    with working_dir("qpid-proton-cpp"):
        check_request_usage("build/request")
        check_respond_usage("build/respond")

        with TestServer() as server:
            with start_process("build/respond {} q1 1", server.connection_url):
                call("build/request {} q1 abc", server.connection_url)

def test_qpid_proton_cpp_auto_create(session):
    with working_dir("qpid-proton-cpp"):
        check_send_usage("build/auto-create/queue-send")
        check_receive_usage("build/auto-create/queue-receive")
        check_send_usage("build/auto-create/topic-send")
        check_receive_usage("build/auto-create/topic-receive")

        with TestServer() as server:
            call("build/auto-create/queue-send {} q1 abc", server.connection_url)
            call("build/auto-create/queue-receive {} q1 1", server.connection_url)
            call("build/auto-create/topic-send {} q2 abc", server.connection_url)
            call("build/auto-create/topic-receive {} q2 1", server.connection_url)

def test_qpid_proton_python_connect(session):
    with working_dir("qpid-proton-python"):
        check_connect_usage("python connect.py")

        with TestServer() as server:
            call("python connect.py {}", server.connection_url)

def test_qpid_proton_python_send_receive(session):
    with working_dir("qpid-proton-python"):
        check_send_usage("python send.py")
        check_receive_usage("python receive.py")

        with TestServer() as server:
            call("python send.py {} q1 abc", server.connection_url)
            call("python receive.py {} q1 1", server.connection_url)

def test_qpid_proton_python_request_respond(session):
    with working_dir("qpid-proton-python"):
        check_request_usage("python request.py")
        check_respond_usage("python respond.py")

        with TestServer() as server:
            with start_process("python respond.py {} q1 1", server.connection_url):
                call("python request.py {} q1 abc", server.connection_url)

def test_qpid_proton_python_auto_create(session):
    with working_dir("qpid-proton-python"):
        check_send_usage("python auto-create/queue-send.py")
        check_receive_usage("auto-create/queue-receive.py")
        check_send_usage("python auto-create/topic-send.py")
        check_receive_usage("python auto-create/topic-receive.py")

        with TestServer() as server:
            call("python auto-create/queue-send.py {} q1 abc", server.connection_url)
            call("python auto-create/queue-receive.py {} q1 1", server.connection_url)
            call("python auto-create/topic-send.py {} q2 abc", server.connection_url)
            call("python auto-create/topic-receive.py {} q2 1", server.connection_url)

def test_qpid_proton_ruby_connect(session):
    with working_dir("qpid-proton-ruby"):
        check_connect_usage("ruby connect.rb")

        with TestServer() as server:
            call("ruby connect.rb {}", server.connection_url)

def test_qpid_proton_ruby_send_receive(session):
    with working_dir("qpid-proton-ruby"):
        check_send_usage("ruby send.rb")
        check_receive_usage("ruby receive.rb")

        with TestServer() as server:
            call("ruby send.rb {} q1 abc", server.connection_url)
            call("ruby receive.rb {} q1 1", server.connection_url)

def test_qpid_proton_ruby_request_respond(session):
    with working_dir("qpid-proton-ruby"):
        check_request_usage("ruby request.rb")
        check_respond_usage("ruby respond.rb")

        with TestServer() as server:
            with start_process("ruby respond.rb {} q1 1", server.connection_url):
                call("ruby request.rb {} q1 abc", server.connection_url)

def test_qpid_proton_ruby_auto_create(session):
    with working_dir("qpid-proton-ruby"):
        check_send_usage("ruby auto-create/queue-send.rb")
        check_receive_usage("auto-create/queue-receive.rb")
        check_send_usage("ruby auto-create/topic-send.rb")
        check_receive_usage("ruby auto-create/topic-receive.rb")

        with TestServer() as server:
            call("ruby auto-create/queue-send.rb {} q1 abc", server.connection_url)
            call("ruby auto-create/queue-receive.rb {} q1 1", server.connection_url)
            call("ruby auto-create/topic-send.rb {} q2 abc", server.connection_url)
            call("ruby auto-create/topic-receive.rb {} q2 1", server.connection_url)

def test_rhea_connect(session):
    with working_dir("rhea"):
        check_connect_usage("node connect.js")

        with TestServer() as server:
            call("node connect.js {}", server.connection_url)

def test_rhea_send_receive(session):
    with working_dir("rhea"):
        check_send_usage("node send.js")
        check_receive_usage("node receive.js")

        with TestServer() as server:
            call("node send.js {} q1 abc", server.connection_url)
            call("node receive.js {} q1 1", server.connection_url)

def test_rhea_request_respond(session):
    with working_dir("rhea"):
        check_request_usage("node request.js")
        check_respond_usage("node respond.js")

        with TestServer() as server:
            with start_process("node respond.js {} q1 1", server.connection_url):
                call("node request.js {} q1 abc", server.connection_url)

def test_rhea_auto_create(session):
    with working_dir("rhea"):
        check_send_usage("node auto-create/queue-send.js")
        check_receive_usage("auto-create/queue-receive.js")
        check_send_usage("node auto-create/topic-send.js")
        check_receive_usage("node auto-create/topic-receive.js")

        with TestServer() as server:
            call("node auto-create/queue-send.js {} q1 abc", server.connection_url)
            call("node auto-create/queue-receive.js {} q1 1", server.connection_url)
            call("node auto-create/topic-send.js {} q2 abc", server.connection_url)
            call("node auto-create/topic-receive.js {} q2 1", server.connection_url)

def test_vertx_proton_send_receive(session):
    with working_dir("vertx-proton"):
        check_send_usage(java_prog("examples.Send"))
        check_receive_usage(java_prog("examples.Receive"))

        with TestServer() as server:
            call("{} {} q1 abc", java_prog("examples.Send"), server.connection_url)
            call("{} {} q1 1", java_prog("examples.Receive"), server.connection_url)

def test_vertx_proton_reactive_streams_send_receive(session):
    with working_dir("vertx-proton"):
        check_send_usage(java_prog("examples.reactivestreams.Send"))
        check_receive_usage(java_prog("examples.reactivestreams.Receive"))

        with TestServer() as server:
            call("{} {} q1 abc", java_prog("examples.reactivestreams.Send"), server.connection_url)
            call("{} {} q1 1", java_prog("examples.reactivestreams.Receive"), server.connection_url)

def test_vertx_proton_makefile(session):
    with working_dir("vertx-proton"):
        with TestServer() as server:
            call("make run URL={}", server.connection_url)

class TestServer(object):
    def __init__(self):
        self.port = random_port()
        self.connection_url = "amqp://127.0.0.1:{}".format(self.port)
        self.output_file = make_temp_file()

        self.output = None
        self.proc = None

    def __enter__(self):
        self.output = open(self.output_file, "w")

        self.proc = start_process("python -m brokerlib 127.0.0.1 {0}", self.port, output=self.output)
        self.proc.connection_url = self.connection_url

        sleep(0.1) # XXX Ugh

        return self.proc

    def __exit__(self, exc_type, exc_value, traceback):
        stop_process(self.proc)

        self.output.flush()
        self.output.close()

        print("-- Server output --")

        for line in read_lines(self.output_file):
            print("> {}".format(line[:-1]))

def check_connect_usage(command):
    usage = None

    try:
        call_for_stderr(command)
    except CalledProcessError as e:
        usage = e.output

    assert usage, usage
    assert "<connection-url>" in usage or "<connection-url>" in usage, usage

def check_send_usage(command):
    usage = None

    try:
        call_for_stderr(command)
    except CalledProcessError as e:
        usage = e.output

    assert usage, usage
    assert "<connection-url> <address> <message-body>" in usage, usage

def check_receive_usage(command):
    usage = None

    try:
        call_for_stderr(command)
    except CalledProcessError as e:
        usage = e.output

    assert usage, usage
    assert "<connection-url> <address> [<message-count>]" in usage, usage

check_request_usage = check_send_usage
check_respond_usage = check_receive_usage

def java_prog(class_name):
    return "java -cp target/classes:target/dependency/\\* {}".format(class_name)

def qpid_jms_prog(class_name):
    return "java -cp target/classes:target/dependency/\\*" \
        " -Djava.naming.factory.initial=org.apache.qpid.jms.jndi.JmsInitialContextFactory" \
        " {}".format(class_name)
