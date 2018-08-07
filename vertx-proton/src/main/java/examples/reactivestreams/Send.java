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
import io.vertx.proton.streams.ProtonStreams;
import io.vertx.proton.streams.ProtonSubscriber;
import java.net.URI;
import java.util.concurrent.CountDownLatch;
import org.apache.qpid.proton.amqp.messaging.AmqpValue;
import org.apache.qpid.proton.message.Message;
import org.reactivestreams.Publisher;
import org.reactivestreams.Subscriber;

public class Send {
    public static void main(String[] args) {
        try {
            if (args.length != 3) {
                System.err.println("Usage: Send <connection-url> <address> <message-body>");
                System.exit(1);
            }

            String url = args[0];
            String address = args[1];
            String messageBody = args[2];

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

                    System.out.println("SEND: Connected to '" + url + "'");

                    ProtonConnection conn = result.result();
                    ProtonSubscriber<Message> subscriber = ProtonStreams.createProducer(conn, address);
                    InputPublisher<Message> publisher = new InputPublisher<>();

                    conn.open();
                    publisher.subscribe(subscriber);
                    publisher.publish(messageBody);

                    System.out.println("SEND: Sent message '" + messageBody + "'");

                    completion.countDown();
                });

            completion.await();
            vertx.close();
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}

class InputPublisher<T extends Message> implements Publisher<T> {
    Subscriber subscriber;
    
    @Override
    public void subscribe(Subscriber<? super T> subscriber) {
        this.subscriber = subscriber;
    }

    public void publish(String messageBody) {
        Message message = Message.Factory.create();
        message.setBody(new AmqpValue(messageBody));

        subscriber.onNext(message);
        subscriber.onComplete();
    }
}
