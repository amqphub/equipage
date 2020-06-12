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

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.util.Hashtable;
import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.MessageConsumer;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.BytesMessage;
import javax.naming.InitialContext;

public class ReceiveFile {
    public static void main(String[] args) {
        try {
            if (args.length != 3) {
                System.err.println("Usage: ReceiveFile <connection-url> <address> <output-file>");
                System.exit(1);
            }

            String url = args[0];
            String address = args[1];
            String outputFilePath = args[2];

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

                BytesMessage message = (BytesMessage) consumer.receive();
                File outputFile = new File(outputFilePath);
                OutputStream outputStream = new FileOutputStream(outputFile);

                int numRead;
                byte buffer[] = new byte[1024];

                for (int pos = 0; pos < message.getBodyLength(); pos += buffer.length) {
                    numRead = message.readBytes(buffer);
                    outputStream.write(buffer, 0, numRead);
                }

                System.out.println("RECEIVE: Received message to file " + outputFilePath);
            } finally {
                conn.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
