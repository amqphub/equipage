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
import java.util.UUID;
import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.MessageConsumer;
import javax.jms.MessageProducer;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.naming.Context;
import javax.naming.InitialContext;

public class Request {
    public static void main(String[] args) {
        try {
            if (args.length != 3) {
                System.err.println("Usage: Request <connection-url> <address> <message-body>");
                System.exit(1);
            }

            String url = args[0];
            String address = args[1];
            String messageBody = args[2];

            Hashtable<Object, Object> env = new Hashtable<>();
            env.put("connectionFactory.factory1", url);

            InitialContext context = new InitialContext(env);
            ConnectionFactory factory = (ConnectionFactory) context.lookup("factory1");
            Connection conn = factory.createConnection();

            conn.start();

            try {
                System.out.println("REQUEST: Connected to '" + url + "'");

                Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
                Queue requestQueue = session.createQueue(address);
                Queue responseQueue = session.createTemporaryQueue();
                MessageProducer producer = session.createProducer(requestQueue);
                MessageConsumer consumer = session.createConsumer(responseQueue);
                TextMessage request = session.createTextMessage();

                System.out.println("REQUEST: Created producer for target address '" + address + "'");

                request.setText(messageBody);
                request.setJMSCorrelationID(UUID.randomUUID().toString());
                request.setJMSReplyTo(responseQueue);

                producer.send(request);

                System.out.println("REQUEST: Sent request '" + request.getText() + "'");

                TextMessage response = (TextMessage) consumer.receive();

                System.out.println("REQUEST: Received response '" + response.getText() + "'");
            } finally {
                conn.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
