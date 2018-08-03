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
import javax.naming.InitialContext;
import org.messaginghub.pooled.jms.JmsPoolConnectionFactory;

public class Configure {
    public static void main(String[] args) {
        try {
            if (args.length != 1) {
                System.err.println("Usage: Configure <connection-url>");
                System.exit(1);
            }

            String url = args[0];

            Hashtable<Object, Object> env = new Hashtable<Object, Object>();
            env.put("connectionfactory.factory1", url);

            InitialContext context = new InitialContext(env);
            ConnectionFactory factory = (ConnectionFactory) context.lookup("factory1");
            JmsPoolConnectionFactory pool = new JmsPoolConnectionFactory();

            try {
                pool.setConnectionFactory(factory);

                // Set the max connections per user to a higher value
                pool.setMaxConnections(5);

                // Create a MessageProducer for each createProducer() call
                pool.setUseAnonymousProducers(false);

                Connection conn = pool.createConnection();

                conn.start();

                try {
                    System.out.println("CONNECT: Connected to '" + url + "'");
                } finally {
                    conn.close();
                }
            } finally {
                pool.stop();
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
