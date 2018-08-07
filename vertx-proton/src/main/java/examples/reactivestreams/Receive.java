/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package examples.reactivestreams;

import io.vertx.core.Vertx;
import io.vertx.proton.ProtonClient;
import io.vertx.proton.ProtonConnection;
import io.vertx.proton.ProtonSender;
import java.io.IOException;
import java.net.URI;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
import org.apache.qpid.proton.amqp.messaging.AmqpValue;
import org.apache.qpid.proton.amqp.messaging.Section;
import org.apache.qpid.proton.message.Message;

import io.vertx.proton.streams.*;
import org.reactivestreams.*;

public class Receive {
    public static void main(String[] args) {
        try {
            if (args.length != 2 && args.length != 3) {
                System.err.println("Usage: Receive <connection-url> <address> [<message-count>]");
                System.exit(1);
            }

            String url = args[0];
            String address = args[1];
            AtomicInteger desired = new AtomicInteger(0);
            AtomicInteger received = new AtomicInteger(0);

            if (args.length == 3) {
                desired.set(Integer.parseInt(args[2]));
            }

            URI uri = new URI(url);
            String host = uri.getHost();
            int port = uri.getPort();

            if (port == -1) {
                port = 5672;
            }

            Vertx vertx = Vertx.vertx();
            ProtonClient client = ProtonClient.create(vertx);
            CountDownLatch completion = new CountDownLatch(1);

            vertx.exceptionHandler((e) -> {
                    e.printStackTrace();
                    System.exit(1);
                });

            client.connect(host, port, (result) -> {
                    if (result.failed()) {
                        throw new RuntimeException(result.cause());
                    }

                    System.out.println("RECEIVE: Connected to '" + url + "'");

                    ProtonConnection conn = result.result();
                    ProtonPublisher<Message> publisher = ProtonStreams.createConsumer
                        (conn, address);
                    OutputSubscriber<Message> subscriber = new OutputSubscriber<>
                        (desired, received, completion);

                    conn.open();
                    publisher.subscribe(subscriber);
                });

            completion.await();
            vertx.close();
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}

class OutputSubscriber<T extends Message> implements Subscriber<T> {
    AtomicInteger desired;
    AtomicInteger received;
    CountDownLatch completion;
    Subscription subscription;

    public OutputSubscriber(AtomicInteger desired, AtomicInteger received,
                            CountDownLatch completion) {
        this.desired = desired;
        this.received = received;
        this.completion = completion;
    }

    @Override
    public void onSubscribe(Subscription subscription) {
        this.subscription = subscription;

        if (desired.get() > 0) {
            this.subscription.request(desired.get());
        }
    }

    @Override
    public void onNext(T t) {
        String body = (String) ((AmqpValue) t.getBody()).getValue();
        System.out.println("RECEIVE: Received message '" + body + "'");

        if (received.incrementAndGet() == desired.get()) {
            subscription.cancel();
            completion.countDown();
        }
    }

    @Override
    public void onError(Throwable t) {
        t.printStackTrace();
        System.exit(1);
    }

    @Override
    public void onComplete() {
        System.err.println(111);
    }
}
