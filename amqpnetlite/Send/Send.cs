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

using System;
using Amqp;

namespace Send
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 3)
            {
                Console.Error.WriteLine("Usage: Send <connection-url> <address> <message-body>");
                Environment.Exit(1);
            }

            string connUrl = args[0];
            string address = args[1];
            string messageBody = args[2];

            Connection conn = new Connection(new Address(connUrl));

            try
            {
                Console.WriteLine("SEND: Connected to '{0}'", connUrl);

                Session session = new Session(conn);
                SenderLink sender = new SenderLink(session, "send-1", address);

                Console.WriteLine("SEND: Created sender for target address '{0}'", address);

                Message message = new Message(messageBody);

                sender.Send(message);

                Console.WriteLine("SEND: Sent message '{0}'", messageBody);
            }
            finally
            {
                conn.Close();
            }
        }
    }
}
