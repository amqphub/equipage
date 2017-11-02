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

package net.ssorj.messaging.examples.jms;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.DeliveryMode;
import javax.jms.MessageConsumer;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;
import org.apache.qpid.jms.JmsConnectionFactory;

public class Receive {
    public static void main(String[] args) throws Exception {
        if (args.length != 2 && args.length != 3) {
            System.err.println("Usage: <prog> CONNECTION-URL ADDRESS [MESSAGE-COUNT]");
            System.exit(1);
        }
        
        String connUrl = args[0];
        String address = args[1];
        int count = Integer.parseInt(args[2]);

        ConnectionFactory connFactory = new JmsConnectionFactory(connUrl);
        Connection conn = connFactory.createConnection();

        System.out.println("RECEIVE: Connected to '" + connUrl + "'");

        conn.start();

        try {
            Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
            Queue queue = session.createQueue(address);
            MessageConsumer consumer = session.createConsumer(queue);

            System.out.println("RECEIVE: Created consumer for source address '" + address + "'");

            for (int i = 0; i < count; i++) {
                TextMessage message = (TextMessage) consumer.receive();

                System.out.println("RECEIVE: Received message '" + message.getText() + "'");
            }
        } finally {
            conn.close();
        }
    }
}
