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

    session.examples_dir = session.module.command.args.examples_dir

def test_amqpnetlite_connect(session):
    with working_dir(join(session.examples_dir, "amqpnetlite")):
        check_connect_usage(dotnet_prog("Connect"))

        with TestServer() as server:
            call("{0} {1}", dotnet_prog("Connect"), server.connection_url)

def test_amqpnetlite_send_receive(session):
    with working_dir(join(session.examples_dir, "amqpnetlite")):
        check_send_usage(dotnet_prog("Send"))
        check_receive_usage(dotnet_prog("Receive"))

        with TestServer() as server:
            call("{0} {1} q1 abc", dotnet_prog("Send"), server.connection_url)
            call("{0} {1} q1 1", dotnet_prog("Receive"), server.connection_url)

def test_amqpnetlite_request_respond(session):
    with working_dir(join(session.examples_dir, "amqpnetlite")):
        check_request_usage(dotnet_prog("Request"))
        check_respond_usage(dotnet_prog("Respond"))

        with TestServer() as server:
            with start_process("{0} {1} q1 1", dotnet_prog("Respond"), server.connection_url):
                call("{0} {1} q1 abc", dotnet_prog("Request"), server.connection_url)

def test_pooled_jms_connect(session):
    with working_dir(join(session.examples_dir, "pooled-jms")):
        check_connect_usage(qpid_jms_prog("examples.Connect"))

        with TestServer() as server:
            call("{0} {1}", qpid_jms_prog("examples.Connect"), server.connection_url)

def test_pooled_jms_configure(session):
    with working_dir(join(session.examples_dir, "pooled-jms")):
        check_connect_usage(qpid_jms_prog("examples.Configure"))

        with TestServer() as server:
            call("{0} {1}", qpid_jms_prog("examples.Configure"), server.connection_url)

def test_qpid_jms_connect(session):
    with working_dir(join(session.examples_dir, "qpid-jms")):
        check_connect_usage(qpid_jms_prog("examples.Connect"))

        with TestServer() as server:
            call("{0} {1}", qpid_jms_prog("examples.Connect"), server.connection_url)

def test_qpid_jms_send_receive(session):
    with working_dir(join(session.examples_dir, "qpid-jms")):
        check_send_usage(qpid_jms_prog("examples.Send"))
        check_receive_usage(qpid_jms_prog("examples.Receive"))

        with TestServer() as server:
            call("{0} {1} q1 abc", qpid_jms_prog("examples.Send"), server.connection_url)
            call("{0} {1} q1 1", qpid_jms_prog("examples.Receive"), server.connection_url)

def test_qpid_jms_request_respond(session):
    with working_dir(join(session.examples_dir, "qpid-jms")):
        check_request_usage(qpid_jms_prog("examples.Request"))
        check_respond_usage(qpid_jms_prog("examples.Respond"))

        with TestServer() as server:
            with start_process("{0} {1} q1 1", qpid_jms_prog("examples.Respond"), server.connection_url):
                call("{0} {1} q1 abc", qpid_jms_prog("examples.Request"), server.connection_url)

def test_qpid_proton_cpp_connect(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_connect_usage("build/connect")

        with TestServer() as server:
            call("build/connect {0}", server.connection_url)

def test_qpid_proton_cpp_send_receive(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_send_usage("build/send")
        check_receive_usage("build/receive")

        with TestServer() as server:
            call("build/send {0} q1 abc", server.connection_url)
            call("build/receive {0} q1 1", server.connection_url)

def test_qpid_proton_cpp_request_respond(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_request_usage("build/request")
        check_respond_usage("build/respond")

        with TestServer() as server:
            with start_process("build/respond {0} q1 1", server.connection_url):
                call("build/request {0} q1 abc", server.connection_url)

def test_qpid_proton_cpp_auto_create(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_send_usage("build/auto-create/queue-send")
        check_receive_usage("build/auto-create/queue-receive")
        check_send_usage("build/auto-create/topic-send")
        check_receive_usage("build/auto-create/topic-receive")

        with TestServer() as server:
            call("build/auto-create/queue-send {0} q1 abc", server.connection_url)
            call("build/auto-create/queue-receive {0} q1 1", server.connection_url)
            call("build/auto-create/topic-send {0} q2 abc", server.connection_url)
            call("build/auto-create/topic-receive {0} q2 1", server.connection_url)

def test_qpid_proton_python_connect(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_connect_usage("python connect.py")

        with TestServer() as server:
            call("python connect.py {0}", server.connection_url)

def test_qpid_proton_python_send_receive(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_send_usage("python send.py")
        check_receive_usage("python receive.py")

        with TestServer() as server:
            call("python send.py {0} q1 abc", server.connection_url)
            call("python receive.py {0} q1 1", server.connection_url)

def test_qpid_proton_python_request_respond(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_request_usage("python request.py")
        check_respond_usage("python respond.py")

        with TestServer() as server:
            with start_process("python respond.py {0} q1 1", server.connection_url):
                call("python request.py {0} q1 abc", server.connection_url)

def test_qpid_proton_python_auto_create(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_send_usage("python auto-create/queue-send.py")
        check_receive_usage("auto-create/queue-receive.py")
        check_send_usage("python auto-create/topic-send.py")
        check_receive_usage("python auto-create/topic-receive.py")

        with TestServer() as server:
            call("python auto-create/queue-send.py {0} q1 abc", server.connection_url)
            call("python auto-create/queue-receive.py {0} q1 1", server.connection_url)
            call("python auto-create/topic-send.py {0} q2 abc", server.connection_url)
            call("python auto-create/topic-receive.py {0} q2 1", server.connection_url)

def test_qpid_proton_ruby_connect(session):
    with working_dir(join(session.examples_dir, "qpid-proton-ruby")):
        check_connect_usage("ruby connect.rb")

        with TestServer() as server:
            call("ruby connect.rb {0}", server.connection_url)

def test_qpid_proton_ruby_send_receive(session):
    with working_dir(join(session.examples_dir, "qpid-proton-ruby")):
        check_send_usage("ruby send.rb")
        check_receive_usage("ruby receive.rb")

        with TestServer() as server:
            call("ruby send.rb {0} q1 abc", server.connection_url)
            call("ruby receive.rb {0} q1 1", server.connection_url)

def test_qpid_proton_ruby_request_respond(session):
    with working_dir(join(session.examples_dir, "qpid-proton-ruby")):
        check_request_usage("ruby request.rb")
        check_respond_usage("ruby respond.rb")

        with TestServer() as server:
            with start_process("ruby respond.rb {0} q1 1", server.connection_url):
                call("ruby request.rb {0} q1 abc", server.connection_url)

def test_qpid_proton_ruby_auto_create(session):
    with working_dir(join(session.examples_dir, "qpid-proton-ruby")):
        check_send_usage("ruby auto-create/queue-send.rb")
        check_receive_usage("auto-create/queue-receive.rb")
        check_send_usage("ruby auto-create/topic-send.rb")
        check_receive_usage("ruby auto-create/topic-receive.rb")

        with TestServer() as server:
            call("ruby auto-create/queue-send.rb {0} q1 abc", server.connection_url)
            call("ruby auto-create/queue-receive.rb {0} q1 1", server.connection_url)
            call("ruby auto-create/topic-send.rb {0} q2 abc", server.connection_url)
            call("ruby auto-create/topic-receive.rb {0} q2 1", server.connection_url)

def test_rhea_connect(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_connect_usage("node connect.js")

        with TestServer() as server:
            call("node connect.js {0}", server.connection_url)

def test_rhea_send_receive(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_send_usage("node send.js")
        check_receive_usage("node receive.js")

        with TestServer() as server:
            call("node send.js {0} q1 abc", server.connection_url)
            call("node receive.js {0} q1 1", server.connection_url)

def test_rhea_request_respond(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_request_usage("node request.js")
        check_respond_usage("node respond.js")

        with TestServer() as server:
            with start_process("node respond.js {0} q1 1", server.connection_url):
                call("node request.js {0} q1 abc", server.connection_url)

def test_rhea_auto_create(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_send_usage("node auto-create/queue-send.js")
        check_receive_usage("auto-create/queue-receive.js")
        check_send_usage("node auto-create/topic-send.js")
        check_receive_usage("node auto-create/topic-receive.js")

        with TestServer() as server:
            call("node auto-create/queue-send.js {0} q1 abc", server.connection_url)
            call("node auto-create/queue-receive.js {0} q1 1", server.connection_url)
            call("node auto-create/topic-send.js {0} q2 abc", server.connection_url)
            call("node auto-create/topic-receive.js {0} q2 1", server.connection_url)

def test_vertx_proton_send_receive(session):
    with working_dir(join(session.examples_dir, "vertx-proton")):
        check_send_usage(java_prog("examples.Send"))
        check_receive_usage(java_prog("examples.Receive"))

        with TestServer() as server:
            call("{0} {1} q1 abc", java_prog("examples.Send"), server.connection_url)
            call("{0} {1} q1 1", java_prog("examples.Receive"), server.connection_url)

def test_vertx_proton_reactive_streams_send_receive(session):
    with working_dir(join(session.examples_dir, "vertx-proton")):
        check_send_usage(java_prog("examples.reactivestreams.Send"))
        check_receive_usage(java_prog("examples.reactivestreams.Receive"))

        with TestServer() as server:
            call("{0} {1} q1 abc", java_prog("examples.reactivestreams.Send"), server.connection_url)
            call("{0} {1} q1 1", java_prog("examples.reactivestreams.Receive"), server.connection_url)

class TestServer(object):
    def __init__(self):
        self.port = random_port()
        self.connection_url = "amqp://127.0.0.1:{0}".format(self.port)
        self.output_file = make_temp_file()

        self.output = None
        self.proc = None

    def __enter__(self):
        self.output = open(self.output_file, "w")

        self.proc = start_process("python -m brokerlib 127.0.0.1 {0}", self.port, output=self.output)
        self.proc.connection_url = self.connection_url

        sleep(0.2) # XXX Ugh

        return self.proc

    def __exit__(self, exc_type, exc_value, traceback):
        stop_process(self.proc)

        self.output.flush()
        self.output.close()

        print("-- Server output --")

        for line in read_lines(self.output_file):
            print("> {0}".format(line[:-1]))

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

def dotnet_prog(project_dir):
    return "dotnet run --project {0}".format(project_dir)

def java_prog(class_name):
    return "java -cp target/classes:target/dependency/\\* {0}".format(class_name)

def qpid_jms_prog(class_name):
    return "java -cp target/classes:target/dependency/\\*" \
        " -Djava.naming.factory.initial=org.apache.qpid.jms.jndi.JmsInitialContextFactory" \
        " {0}".format(class_name)
