# Vert.x Proton examples

## Building the examples

```sh
mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests
```

## Running the examples

```sh
# Run an AMQP broker with a queue named 'queue1' listening on localhost on port 5672
java -cp target/classes:target/dependency/\* examples.Send amqp://localhost queue1 message1
java -cp target/classes:target/dependency/\* examples.Receive amqp://localhost queue1 1
java -cp target/classes:target/dependency/\* examples.Send amqp://localhost queue1 message1
java -cp target/classes:target/dependency/\* examples.Send amqp://localhost queue1 1
```
