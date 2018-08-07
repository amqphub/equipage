.PHONY: build
build:
	mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests

.PHONY: run
run: COMMAND := java -cp target/classes:target/dependency/\*
run: URL := amqp://localhost
run:
	${COMMAND} examples.Send ${URL} q0 abc
	${COMMAND} examples.Receive ${URL} q0 1
	${COMMAND} examples.reactivestreams.Send ${URL} q0 abc
	${COMMAND} examples.reactivestreams.Receive ${URL} q0 1

.PHONY: clean
clean:
	rm -rf target
	rm -rf .vertx
