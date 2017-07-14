import java.lang.RuntimeException;
import javax.jms.*;
import javax.naming.*;

public class Requester {
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
            Destination responseQueue = session.createTemporaryQueue();
            MessageProducer producer = session.createProducer(requestQueue);
            MessageConsumer consumer = session.createConsumer(responseQueue);

            producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);

            TextMessage request = session.createTextMessage();

            request.setText("abc");
            request.setJMSReplyTo(responseQueue);

            System.out.println("REQUESTER: Sent request '" + request.getText() + "'");

            producer.send(request);
            
            TextMessage response = (TextMessage) consumer.receive();

            if (response == null) {
                throw new RuntimeException("Null response");
            }

            System.out.println("REQUESTER: Received response: '" + response.getText() + "'");
        } catch (JMSException e) {
            throw new RuntimeException(e);
        }
    }
}
