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
using Amqp.Framing;
using Amqp.Types;

namespace QueueReceive
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 2 && args.Length != 3)
            {
                Console.Error.WriteLine("Usage: QueueReceive <connection-url> <address> [<message-count>]");
                Environment.Exit(1);
            }

            string connUrl = args[0];
            string address = args[1];
            int desired = 0;
            int received = 0;

            if (args.Length == 3)
            {
                desired = Int32.Parse(args[2]);
            }

            Connection conn = new Connection(new Address(connUrl));

            try
            {
                Session session = new Session(conn);

                Source source = new Source() {
                    Address = address,
                    Capabilities = new Symbol[] {"queue"},
                };

                OnAttached onAttached = (link, attach) =>
                {
                    Console.WriteLine("RECEIVE: Opened receiver for source address '{0}'", address);
                };

                ReceiverLink receiver = new ReceiverLink(session, "r1", source, onAttached);

                while (true)
                {
                    Message message = receiver.Receive();
                    receiver.Accept(message);

                    Console.WriteLine("RECEIVE: Received message '{0}'", message.Body);

                    received++;

                    if (received == desired)
                    {
                        break;
                    }
                }
            }
            finally
            {
                conn.Close();
            }
        }
    }
}
