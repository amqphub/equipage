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

import sys as _sys

from brokerlib import wait_for_broker
from commandant import TestSkipped
from plano import *

def open_test_session(session):
    enable_logging(level="error")

    session.examples_dir = session.module.command.args.examples_dir
    session.test_timeout = 120

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

def test_amqpnetlite_auto_create(session):
    with working_dir(join(session.examples_dir, "amqpnetlite")):
        check_send_usage(dotnet_prog("AutoCreate/QueueSend"))
        check_receive_usage(dotnet_prog("AutoCreate/QueueReceive"))
        check_send_usage(dotnet_prog("AutoCreate/TopicSend"))
        check_receive_usage(dotnet_prog("AutoCreate/TopicReceive"))

        with TestServer() as server:
            call("{0} {1} q1 abc", dotnet_prog("AutoCreate/QueueSend"), server.connection_url)
            call("{0} {1} q1 1", dotnet_prog("AutoCreate/QueueReceive"), server.connection_url)
            call("{0} {1} t1 abc", dotnet_prog("AutoCreate/TopicSend"), server.connection_url)
            call("{0} {1} t1 1", dotnet_prog("AutoCreate/TopicReceive"), server.connection_url)

def test_amqpnetlite_subscriptions(session):
    with working_dir(join(session.examples_dir, "amqpnetlite")):
        check_receive_usage(dotnet_prog("Subscriptions/DurableSubscribe"))
        check_receive_usage(dotnet_prog("Subscriptions/SharedSubscribe"))
        check_receive_usage(dotnet_prog("Subscriptions/DurableSharedSubscribe"))

        with TestServer() as server:
            call("{0} {1} t1 abc", dotnet_prog("Send"), server.connection_url)
            call("{0} {1} t1 1", dotnet_prog("Subscriptions/DurableSubscribe"), server.connection_url)
            call("{0} {1} t1 abc", dotnet_prog("Send"), server.connection_url)
            call("{0} {1} t1 1", dotnet_prog("Subscriptions/SharedSubscribe"), server.connection_url)
            call("{0} {1} t1 abc", dotnet_prog("Send"), server.connection_url)
            call("{0} {1} t1 1", dotnet_prog("Subscriptions/DurableSharedSubscribe"), server.connection_url)

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
    with working_dir(join(session.examples_dir, "qpid-jms/basic")):
        check_connect_usage(qpid_jms_prog("examples.Connect"))

        with TestServer() as server:
            call("{0} {1}", qpid_jms_prog("examples.Connect"), server.connection_url)

def test_qpid_jms_send_receive(session):
    with working_dir(join(session.examples_dir, "qpid-jms/basic")):
        check_send_usage(qpid_jms_prog("examples.Send"))
        check_receive_usage(qpid_jms_prog("examples.Receive"))

        with TestServer() as server:
            call("{0} {1} q1 abc", qpid_jms_prog("examples.Send"), server.connection_url)
            call("{0} {1} q1 1", qpid_jms_prog("examples.Receive"), server.connection_url)

def test_qpid_jms_request_respond(session):
    with working_dir(join(session.examples_dir, "qpid-jms/basic")):
        check_request_usage(qpid_jms_prog("examples.Request"))
        check_respond_usage(qpid_jms_prog("examples.Respond"))

        with TestServer() as server:
            with start_process("{0} {1} q1 1", qpid_jms_prog("examples.Respond"), server.connection_url):
                call("{0} {1} q1 abc", qpid_jms_prog("examples.Request"), server.connection_url)

def test_qpid_jms_message_content(session):
    with working_dir(join(session.examples_dir, "qpid-jms/message-content")):
        with TestServer() as server:
            with temp_file() as temp:
                input_data = "x" * 2049
                write(temp, input_data)

                with start_process("{0} {1} q1 {2}", qpid_jms_prog("examples.ReceiveFile"), server.connection_url, temp):
                    call("{0} {1} q1 {2}", qpid_jms_prog("examples.SendFile"), server.connection_url, temp)

                output_data = read(temp)
                assert input_data == output_data

def test_qpid_jms_tracing(session):
    with working_dir(join(session.examples_dir, "qpid-jms/tracing")):
        check_send_usage(qpid_jms_prog("examples.Send"))
        check_receive_usage(qpid_jms_prog("examples.Receive"))

        with TestServer() as server:
            url = server.connection_url + "?jms.tracing=opentracing"

            with working_env(JAEGER_SAMPLER_TYPE="const", JAEGER_SAMPLER_PARAM="1"):
                call("{0} {1} q1 abc", qpid_jms_prog("examples.Send"), url)
                call("{0} {1} q1 1", qpid_jms_prog("examples.Receive"), url)

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

def test_qpid_proton_cpp_servers(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_receive_usage("build/servers/receive")

        connection_url = "amqp://localhost:{0}".format(random_port())

        with start_process("build/servers/receive {0} q1 1", connection_url):
            sleep(1)
            call("build/send {0} q1 abc", connection_url)

def test_qpid_proton_cpp_auto_create(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_send_usage("build/auto-create/queue-send")
        check_receive_usage("build/auto-create/queue-receive")
        check_send_usage("build/auto-create/topic-send")
        check_receive_usage("build/auto-create/topic-receive")

        with TestServer() as server:
            call("build/auto-create/queue-send {0} q1 abc", server.connection_url)
            call("build/auto-create/queue-receive {0} q1 1", server.connection_url)
            call("build/auto-create/topic-send {0} t1 abc", server.connection_url)
            call("build/auto-create/topic-receive {0} t1 1", server.connection_url)

def test_qpid_proton_cpp_message_groups(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        with TestServer() as server:
            call("build/message-groups/send {0} q1 10 group1", server.connection_url)
            call("build/receive {0} q1 10", server.connection_url)

def test_qpid_proton_cpp_threading(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_send_usage("build/threading/send")
        check_receive_usage("build/threading/receive")

        with TestServer() as server:
            call("build/threading/send {0} q1 abc", server.connection_url)
            call("build/threading/receive {0} q1 1", server.connection_url)

            call("build/threading/send {0} q1 abc1", server.connection_url)
            call("build/threading/send {0} q1 abc2", server.connection_url)
            call("build/threading/send {0} q1 abc3", server.connection_url)
            call("build/threading/receive {0} q1 3", server.connection_url)

            call("build/threading/send {0} q1 abc", server.connection_url)
            call("build/threading/receive-acknowledge {0} q1 1", server.connection_url)

            call("build/threading/send {0} q1 abc1", server.connection_url)
            call("build/threading/send {0} q1 abc2", server.connection_url)
            call("build/threading/send {0} q1 abc3", server.connection_url)
            call("build/threading/receive-acknowledge {0} q1 3", server.connection_url)

def test_qpid_proton_cpp_subscriptions(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):
        check_receive_usage("build/subscriptions/durable-subscribe")
        check_receive_usage("build/subscriptions/shared-subscribe")
        check_receive_usage("build/subscriptions/durable-shared-subscribe")

        with TestServer() as server:
            call("build/send {0} t1 abc", server.connection_url)
            call("build/subscriptions/durable-subscribe {0} t1 1", server.connection_url)
            call("build/send {0} t1 abc", server.connection_url)
            call("build/subscriptions/shared-subscribe {0} t1 1", server.connection_url)
            call("build/send {0} t1 abc", server.connection_url)
            call("build/subscriptions/durable-shared-subscribe {0} t1 1", server.connection_url)

def test_qpid_proton_cpp_link_failure_recovery(session):
    with working_dir(join(session.examples_dir, "qpid-proton-cpp")):

        # These tests do not use a broker, they have senders and listeners that
        # connect directly to each other.

        # Test where receiver closes link, sender must handle error
        port = get_random_port()
        with start_process("build/reconnect/receiver-close-link 127.0.0.1:{0} lf1", port):
            call("build/reconnect/sender-handle-link-err 127.0.0.1:{0} lf1", port)
        # Test where sender closes link, receiver must handle error
        port = get_random_port()
        with start_process("build/reconnect/receiver-handle-link-err 127.0.0.1:{0} lf2", port):
            call("build/reconnect/sender-close-link 127.0.0.1:{0} lf2", port)

def test_qpid_proton_python_connect(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_connect_usage(python_prog("connect.py"))

        with TestServer() as server:
            call("{0} {1}", python_prog("connect.py"), server.connection_url)

def test_qpid_proton_python_send_receive(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_send_usage(python_prog("send.py"))
        check_receive_usage(python_prog("receive.py"))

        with TestServer() as server:
            call("{0} {1} q1 abc", python_prog("send.py"), server.connection_url)
            call("{0} {1} q1 1", python_prog("receive.py"), server.connection_url)

def test_qpid_proton_python_request_respond(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_request_usage(python_prog("request.py"))
        check_respond_usage(python_prog("respond.py"))

        with TestServer() as server:
            with start_process("{0} {1} q1 1", python_prog("respond.py"), server.connection_url):
                call("{0} {1} q1 abc", python_prog("request.py"), server.connection_url)

def test_qpid_proton_python_servers(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_receive_usage(python_prog("servers/receive.py"))

        connection_url = "amqp://localhost:{0}".format(random_port())

        with start_process("{0} {1} q1 1", python_prog("servers/receive.py"), connection_url):
            sleep(1)
            call("{0} {1} q1 abc", python_prog("send.py"), connection_url)

def test_qpid_proton_python_auto_create(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_send_usage(python_prog("auto-create/queue-send.py"))
        check_receive_usage(python_prog("auto-create/queue-receive.py"))
        check_send_usage(python_prog("auto-create/topic-send.py"))
        check_receive_usage(python_prog("auto-create/topic-receive.py"))

        with TestServer() as server:
            call("{0} {1} q1 abc", python_prog("auto-create/queue-send.py"), server.connection_url)
            call("{0} {1} q1 1", python_prog("auto-create/queue-receive.py"), server.connection_url)
            call("{0} {1} t1 abc", python_prog("auto-create/topic-send.py"), server.connection_url)
            call("{0} {1} t1 1", python_prog("auto-create/topic-receive.py"), server.connection_url)

def test_qpid_proton_python_subscriptions(session):
    with working_dir(join(session.examples_dir, "qpid-proton-python")):
        check_receive_usage(python_prog("subscriptions/durable-subscribe.py"))
        check_receive_usage(python_prog("subscriptions/shared-subscribe.py"))
        check_receive_usage(python_prog("subscriptions/durable-shared-subscribe.py"))

        with TestServer() as server:
            call("{0} {1} t1 abc", python_prog("send.py"), server.connection_url)
            call("{0} {1} t1 1", python_prog("subscriptions/durable-subscribe.py"), server.connection_url)
            call("{0} {1} t1 abc", python_prog("send.py"), server.connection_url)
            call("{0} {1} t1 1", python_prog("subscriptions/shared-subscribe.py"), server.connection_url)
            call("{0} {1} t1 abc", python_prog("send.py"), server.connection_url)
            call("{0} {1} t1 1", python_prog("subscriptions/durable-shared-subscribe.py"), server.connection_url)

def test_qpid_proton_python_tracing(session):
    try:
        import opentracing
        import jaeger_client
    except ImportError:
        raise TestSkipped("The opentracing and jaeger_client libraries are not available")

    with working_dir(join(session.examples_dir, "qpid-proton-python/tracing")):
        check_send_usage(python_prog("send.py"))
        check_receive_usage(python_prog("receive.py"))

        with TestServer() as server:
            call("{0} {1} q1 abc", python_prog("send.py"), server.connection_url)
            call("{0} {1} q1 1", python_prog("receive.py"), server.connection_url)

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
            call("ruby auto-create/topic-send.rb {0} t1 abc", server.connection_url)
            call("ruby auto-create/topic-receive.rb {0} t1 1", server.connection_url)

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

def test_rhea_servers(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_receive_usage("node servers/receive.js")

        connection_url = "amqp://localhost:{0}".format(random_port())

        with start_process("node servers/receive.js {0} q1 1", connection_url):
            sleep(1)
            call("node send.js {0} q1 abc", connection_url)

def test_rhea_acknowledgment(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_send_usage("node send.js")
        check_receive_usage("node acknowledgment/receive.js")

        with TestServer() as server:
            call("node send.js {0} q1 abc", server.connection_url)
            call("node acknowledgment/receive.js {0} q1 1", server.connection_url)

def test_rhea_auto_create(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_send_usage("node auto-create/queue-send.js")
        check_receive_usage("auto-create/queue-receive.js")
        check_send_usage("node auto-create/topic-send.js")
        check_receive_usage("node auto-create/topic-receive.js")

        with TestServer() as server:
            call("node auto-create/queue-send.js {0} q1 abc", server.connection_url)
            call("node auto-create/queue-receive.js {0} q1 1", server.connection_url)
            call("node auto-create/topic-send.js {0} t1 abc", server.connection_url)
            call("node auto-create/topic-receive.js {0} t1 1", server.connection_url)

def test_rhea_subscriptions(session):
    with working_dir(join(session.examples_dir, "rhea")):
        check_receive_usage("subscriptions/durable-subscribe.js")
        check_receive_usage("subscriptions/shared-subscribe.js")
        check_receive_usage("subscriptions/durable-shared-subscribe.js")

        with TestServer() as server:
            call("node send.js {0} t1 abc", server.connection_url)
            call("node subscriptions/durable-subscribe.js {0} t1 1", server.connection_url)
            call("node send.js {0} t1 abc", server.connection_url)
            call("node subscriptions/shared-subscribe.js {0} t1 1", server.connection_url)
            call("node send.js {0} t1 abc", server.connection_url)
            call("node subscriptions/durable-shared-subscribe.js {0} t1 1", server.connection_url)

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

        with temp_file() as ready_file:
            self.proc = start_process("{0} -m brokerlib --host 127.0.0.1 --port {1} --ready-file {2}",
                                      _sys.executable, self.port, ready_file, output=self.output)
            self.proc.connection_url = self.connection_url

            wait_for_broker(ready_file)

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

def python_prog(file):
    return "{0} {1}".format(_sys.executable, file)

def qpid_jms_prog(class_name):
    return "java -cp target/classes:target/dependency/\\*" \
        " -Djava.naming.factory.initial=org.apache.qpid.jms.jndi.JmsInitialContextFactory" \
        " {0}".format(class_name)
