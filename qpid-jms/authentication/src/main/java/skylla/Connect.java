package skylla;

import org.apache.qpid.jms.JmsConnectionFactory;

import javax.jms.*;
import javax.naming.Context;
import java.util.Hashtable;

public class Connect {
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
