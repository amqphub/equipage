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

package examples;

import io.vertx.core.Vertx;
import io.vertx.proton.ProtonClient;
import io.vertx.proton.ProtonConnection;
import io.vertx.proton.ProtonReceiver;
import java.net.URI;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
import org.apache.qpid.proton.amqp.messaging.AmqpValue;
import org.apache.qpid.proton.message.Message;

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

            client.connect(host, port, (connResult) -> {
                    if (connResult.failed()) {
                        throw new RuntimeException(connResult.cause());
                    }

                    ProtonConnection conn = connResult.result();
                    ProtonReceiver receiver = conn.createReceiver(address);

                    receiver.openHandler((result) -> {
                            System.out.println("RECEIVE: Opened receiver for source address " +
                                               "'" + address + "'");
                        });
                    
                    receiver.handler((delivery, message) -> {
                            String body = (String) ((AmqpValue) message.getBody()).getValue();
                            
                            System.out.println("RECEIVE: Received message '" + body + "'");

                            if (received.incrementAndGet() == desired.get()) {
                                conn.close();
                            }
                        });

                    conn.closeHandler((result) -> {
                            completion.countDown();
                        });

                    conn.open();
                    receiver.open();
                });

            completion.await();
            vertx.close();
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
