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

package examples.authentication;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import org.apache.qpid.jms.JmsConnectionFactory;

public class Kerberos {
    public static void main(String[] args) {
        try {
            if (args.length != 1) {
                System.err.println("Usage: Kerberos <connection-url>");
                System.exit(1);
            }
            
            String url = args[0] + "?amqp.saslMechanisms=GSSAPI";
            ConnectionFactory factory = new JmsConnectionFactory(url);
            Connection conn = factory.createConnection("alice", "secret");

            conn.start();
            
            try {
                System.out.println("CONNECT: Connected to '" + url + "'");
            } finally {
                conn.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
