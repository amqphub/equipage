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

import javax.jms.*;
import javax.naming.*;

public class Receive {
    public static void main(String[] args) throws Exception {
        Context context = new InitialContext();
        ConnectionFactory factory = (ConnectionFactory) context.lookup("example");
        Destination queue = (Destination) context.lookup("example1");
        Connection connection = factory.createConnection("guest", "guest");

        connection.start();

        try {
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageConsumer messageConsumer = session.createConsumer(queue);

            while (true) {
                TextMessage message = (TextMessage) messageConsumer.receive();

                System.out.println("receiver: " + message.getText());
            }
        } finally {
            connection.close();
        }
    }
}
