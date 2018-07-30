.PHONY: build
build:
	mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests

.PHONY: run
run:
	java -cp "target/classes:target/dependency/*" examples.Connect amqp://localhost
	java -cp "target/classes:target/dependency/*" examples.Send amqp://localhost examples message1
	java -cp "target/classes:target/dependency/*" examples.Receive amqp://localhost examples 1

.PHONY: clean
clean:
	rm -rf target
