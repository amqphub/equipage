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

public class Requester {
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
            Destination responseQueue = session.createTemporaryQueue();
            MessageProducer producer = session.createProducer(requestQueue);
            MessageConsumer consumer = session.createConsumer(responseQueue);

            producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);

            TextMessage request = session.createTextMessage();

            request.setText("abc");
            request.setJMSReplyTo(responseQueue);

            System.out.println("REQUESTER: Sent request '" + request.getText() + "'");

            producer.send(request);
            
            TextMessage response = (TextMessage) consumer.receive();

            if (response == null) {
                throw new RuntimeException("Null response");
            }

            System.out.println("REQUESTER: Received response: '" + response.getText() + "'");
        } catch (JMSException e) {
            throw new RuntimeException(e);
        }
    }
}
