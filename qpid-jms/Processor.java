import java.lang.RuntimeException;
import javax.jms.*;
import javax.naming.*;

public class Processor {
    public static void main(String[] args) {
        ConnectionFactory factory;
        Destination requestQueue;

        try {
            Context context = new InitialContext();
            factory = (ConnectionFactory) context.lookup("factoryLookup");
            requestQueue = (Destination) context.lookup("requestQueueLookup");
        } catch (NamingException e) {
            throw new RuntimeException(e);
        }

        try {
            Connection connection = factory.createConnection();

            connection.start();

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer producer = session.createProducer(null);
            MessageConsumer consumer = session.createConsumer(requestQueue);

            producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);

            while (true) {
                TextMessage request = (TextMessage) consumer.receive(1);

                if (request == null) {
                    continue;
                }

                System.out.println("PROCESSOR: Received request '" + request.getText() + "'");

                String processedText = request.getText().toUpperCase();
                TextMessage response = session.createTextMessage();

                response.setText(processedText);
                producer.send(request.getJMSReplyTo(), response);

                System.out.println("PROCESSOR: Sent response '" + processedText + "'");
            }
        } catch (JMSException e) {
            throw new RuntimeException(e);
        }
    }
}
