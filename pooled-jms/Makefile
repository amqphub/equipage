.PHONY: build
build:
	mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests

.PHONY: run
run: COMMAND := java -cp target/classes:target/dependency/\* -Djava.naming.factory.initial=org.apache.qpid.jms.jndi.JmsInitialContextFactory
run: URL := amqp://localhost
run:
	${COMMAND} examples.Connect ${URL}
	${COMMAND} examples.Configure ${URL}

.PHONY: clean
clean:
	rm -rf target
