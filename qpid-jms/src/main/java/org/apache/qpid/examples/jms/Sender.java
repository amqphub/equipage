package com.redhat.messaging.example;

import javax.jms.*;
import javax.naming.*;

public class Sender {
    public static void main(String[] args) throws Exception {
        Context context = new InitialContext();
        ConnectionFactory factory = (ConnectionFactory) context.lookup("example");
        Destination queue = (Destination) context.lookup("example1");
        Connection connection = factory.createConnection("guest", "guest");

        connection.start();

        try {
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer messageProducer = session.createProducer(queue);

            while (true) {
                System.out.print("sender> ");
                
                String line = System.console().readLine();
                TextMessage message = session.createTextMessage(line);
            
                messageProducer.send(message,
                                     DeliveryMode.NON_PERSISTENT,
                                     Message.DEFAULT_PRIORITY,
                                     Message.DEFAULT_TIME_TO_LIVE);
            }
        } finally {
            connection.close();
        }
    }
}
