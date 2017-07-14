package com.redhat.messaging.example;

import javax.jms.*;
import javax.naming.*;

public class Receiver {
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
