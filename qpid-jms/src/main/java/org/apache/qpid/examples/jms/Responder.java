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

package org.apache.qpid.examples.jms;

import java.lang.RuntimeException;
import javax.jms.*;
import javax.naming.*;

public class Responder {
    public static void main(String[] args) {
        ConnectionFactory factory;
        Destination requestQueue;

        try {
            Context context = new InitialContext();
            factory = (ConnectionFactory) context.lookup("factoryLookup");
            requestQueue = (Destination) context.lookup("requestQueueLookup");
        } catch (NamingException e) {
            throw new RuntimeException(e);
        }

        try {
            Connection connection = factory.createConnection();

            connection.start();

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer producer = session.createProducer(null);
            MessageConsumer consumer = session.createConsumer(requestQueue);

            producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);

            while (true) {
                TextMessage request = (TextMessage) consumer.receive(1);

                if (request == null) {
                    continue;
                }

                System.out.println("RESPONDER: Received request '" + request.getText() + "'");

                String processedText = request.getText().toUpperCase();
                TextMessage response = session.createTextMessage();

                response.setText(processedText);
                producer.send(request.getJMSReplyTo(), response);

                System.out.println("RESPONDER: Sent response '" + processedText + "'");
            }
        } catch (JMSException e) {
            throw new RuntimeException(e);
        }
    }
}
