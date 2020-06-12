/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */

package examples;

import java.util.Hashtable;
import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.MessageConsumer;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.naming.InitialContext;

public class Receive {
    public static void main(String[] args) {
        try {
            if (args.length != 2 && args.length != 3) {
                System.err.println("Usage: Receive <connection-url> <address> [<message-count>]");
                System.exit(1);
            }

            String url = args[0];
            String address = args[1];
            int desired = 0;
            int received = 0;

            if (args.length == 3) {
                desired = Integer.parseInt(args[2]);
            }

            Hashtable<Object, Object> env = new Hashtable<>();
            env.put("connectionFactory.factory1", url);

            InitialContext context = new InitialContext(env);
            ConnectionFactory factory = (ConnectionFactory) context.lookup("factory1");
            Connection conn = factory.createConnection();

            conn.start();

            try {
                System.out.println("RECEIVE: Connected to '" + url + "'");

                Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
                Queue queue = session.createQueue(address);
                MessageConsumer consumer = session.createConsumer(queue);

                System.out.println("RECEIVE: Created consumer for source address '" + address + "'");

                while (true) {
                    TextMessage message = (TextMessage) consumer.receive();

                    System.out.println("RECEIVE: Received message '" + message.getText() + "'");

                    received++;

                    if (received == desired) {
                        break;
                    }
                }
            } finally {
                conn.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
