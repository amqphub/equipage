.PHONY: build
build:
	mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests

.PHONY: run
run:
	java -cp "target/classes:target/dependency/*" net.ssorj.messaging.examples.jms.Connect

.PHONY: clean
clean:
	rm -rf target
