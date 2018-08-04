.PHONY: build
build:
	mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests

.PHONY: run
run: COMMAND := java -cp target/classes:target/dependency/\*
run: URL := amqp://localhost
run:
	${COMMAND} examples.Send ${URL}
	${COMMAND} examples.Receive ${URL}

.PHONY: clean
clean:
	rm -rf target
	rm -rf .vertx
