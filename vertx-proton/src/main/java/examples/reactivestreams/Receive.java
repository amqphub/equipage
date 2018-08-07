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
import io.vertx.proton.streams.ProtonPublisher;
import io.vertx.proton.streams.ProtonStreams;
import java.net.URI;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
import org.apache.qpid.proton.amqp.messaging.AmqpValue;
import org.apache.qpid.proton.message.Message;
import org.reactivestreams.Subscriber;
import org.reactivestreams.Subscription;

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

            client.connect(host, port, (connResult) -> {
                    if (connResult.failed()) {
                        throw new RuntimeException(connResult.cause());
                    }

                    System.out.println("RECEIVE: Connected to '" + url + "'");

                    ProtonConnection conn = connResult.result();
                    ProtonPublisher<Message> publisher = ProtonStreams.createConsumer
                        (conn, address);
                    OutputSubscriber<Message> subscriber = new OutputSubscriber<>
                        (conn, desired);

                    conn.closeHandler((result) -> {
                            completion.countDown();
                        });

                    publisher.subscribe(subscriber);

                    conn.open();
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
    static final int WINDOW_SIZE = 10;

    ProtonConnection connection;
    Subscription subscription;
    AtomicInteger received = new AtomicInteger(0);
    AtomicInteger desired;

    public OutputSubscriber(ProtonConnection connection, AtomicInteger desired) {
        this.connection = connection;
        this.desired = desired;
    }

    @Override
    public void onSubscribe(Subscription subscription) {
        this.subscription = subscription;
        this.subscription.request(WINDOW_SIZE);
    }

    @Override
    public void onNext(T t) {
        String body = (String) ((AmqpValue) t.getBody()).getValue();

        System.out.println("RECEIVE: Received message '" + body + "'");

        int rc = received.incrementAndGet();
        int dc = desired.get();

        if (rc % WINDOW_SIZE == 0 && rc < dc) {
            if (dc - rc >= WINDOW_SIZE) {
                subscription.request(WINDOW_SIZE);
            } else {
                subscription.request(dc - rc);
            }
        } else if (rc == dc) {
            subscription.cancel();
            connection.close();
        }
    }

    @Override
    public void onError(Throwable t) {
        t.printStackTrace();
        System.exit(1);
    }

    @Override
    public void onComplete() {
        connection.close();
    }
}
