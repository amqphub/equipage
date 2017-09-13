default: test

.PHONY: build
build:
	mvn package

.PHONY: clean
clean:
	mvn clean

.PHONY: test
test: build
	java -classpath target/skylla-1.0.0-SNAPSHOT-jar-with-dependencies.jar -Djava.security.auth.login.config=src/main/resources/login.config -Dsun.security.krb5.debug=true skylla.Connect upto.nogood.industries
