.PHONY: build
build:
	mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests

.PHONY: run
run: URL := amqp://localhost
run:
	scripts/run examples.Connect ${URL}
	scripts/run examples.Send ${URL} examples message1
	scripts/run examples.Receive ${URL} examples 1

.PHONY: clean
clean:
	rm -rf target
