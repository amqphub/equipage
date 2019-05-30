# Pooled JMS examples

## Building the examples

```sh
mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests
```

## Running the examples

```sh
# Run an AMQP server listening on localhost on port 5672

java -cp target/classes:target/dependency/\* \
   -Djava.naming.factory.initial=org.apache.qpid.jms.jndi.JmsInitialContextFactory \
   examples.Connect amqp://localhost

java -cp target/classes:target/dependency/\* \
   -Djava.naming.factory.initial=org.apache.qpid.jms.jndi.JmsInitialContextFactory \
   examples.Configure amqp://localhost
```
