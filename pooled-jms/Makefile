.PHONY: build
build:
	mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests

.PHONY: run
run: URL := amqp://localhost
run:
	scripts/run examples.Connect ${URL}
	scripts/run examples.Configure ${URL}

.PHONY: clean
clean:
	rm -rf target
