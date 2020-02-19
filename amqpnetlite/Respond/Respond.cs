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

namespace Respond
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 2 && args.Length != 3)
            {
                Console.Error.WriteLine("Usage: Respond <connection-url> <address> [<message-count>]");
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

                OnAttached onSenderAttached = (link, attach) =>
                {
                    Console.WriteLine("RESPOND: Opened anonymous sender for responses");
                };

                SenderLink sender = new SenderLink(session, "s1", (Target) null, onSenderAttached);

                Source source = new Source()
                {
                    Address = address,
                };

                OnAttached onReceiverAttached = (link, attach) =>
                {
                    Console.WriteLine("RESPOND: Opened receiver for source address '{0}'", address);
                };

                ReceiverLink receiver = new ReceiverLink(session, "r1", source, onReceiverAttached);

                while (true)
                {
                    Message request = receiver.Receive();
                    receiver.Accept(request);

                    Console.WriteLine("RESPOND: Received request '{0}'", request.Body);

                    string responseBody = ((string) request.Body).ToUpper();

                    Message response = new Message(responseBody);

                    response.Properties = new Properties()
                    {
                        To = request.Properties.ReplyTo,
                        CorrelationId = request.Properties.MessageId,
                    };

                    sender.Send(response);

                    Console.WriteLine("RESPOND: Sent response '{0}'", response.Body);

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
