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
import javax.jms.MessageProducer;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.naming.InitialContext;

public class Respond {
    public static void main(String[] args) {
        try {
            if (args.length != 2 && args.length != 3) {
                System.err.println("Usage: Respond <connection-url> <address> [<message-count>]");
                System.exit(1);
            }

            String url = args[0];
            String address = args[1];
            int desired = 0;
            int received = 0;

            if (args.length == 3) {
                desired = Integer.parseInt(args[2]);
            }
            
            Hashtable<Object, Object> env = new Hashtable<Object, Object>();
            env.put("connectionfactory.factory1", url);
            
            InitialContext context = new InitialContext(env);
            ConnectionFactory factory = (ConnectionFactory) context.lookup("factory1");
            Connection conn = factory.createConnection();

            conn.start();

            try {
                System.out.println("RESPOND: Connected to '" + url + "'");
                
                Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
                Queue queue = session.createQueue(address);
                MessageProducer producer = session.createProducer(null);
                MessageConsumer consumer = session.createConsumer(queue);

                System.out.println("RESPOND: Created consumer for source address '" + address + "'");
                
                while (true) {
                    TextMessage request = (TextMessage) consumer.receive();

                    System.out.println("RESPOND: Received request '" + request.getText() + "'");

                    String responseBody = request.getText().toUpperCase();
                    TextMessage response = session.createTextMessage();

                    response.setText(responseBody);
                    response.setJMSCorrelationID(request.getJMSMessageID());

                    producer.send(request.getJMSReplyTo(), response);

                    System.out.println("RESPOND: Sent response '" + response.getText() + "'");

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
