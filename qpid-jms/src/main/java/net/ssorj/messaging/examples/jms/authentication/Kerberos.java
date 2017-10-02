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

package net.ssorj.messaging.examples.jms.authentication;

import org.apache.qpid.jms.JmsConnectionFactory;

import javax.jms.*;
import javax.naming.Context;
import java.util.Hashtable;

public class Kerberos {
    public static void main(String[] args) throws Exception {
        String authority = args[0];
        
        Connection connection = null;
        ConnectionFactory connectionFactory = new JmsConnectionFactory("amqp://" + authority + "?amqp.saslMechanisms=GSSAPI");

        try {
            connection = connectionFactory.createConnection();
            System.out.println("Connected!");
        } finally {
            if (connection != null) {
                connection.close();
            }
        }
    }
}
