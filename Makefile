.NOTPARALLEL:

export PYTHONPATH := ${CURDIR}/python

.PHONY: build
build:
	cd pooled-jms && make build
	cd qpid-jms && make build
	cd qpid-proton-cpp && make build
	cd qpid-proton-python && make build
	cd rhea && make build
	cd vertx-proton && make build

.PHONY: test
test: build
	scripts/test --timeout 10

.PHONY: big-test
big-test: test test-centos-7

.PHONY: test-centos-7
test-centos-7: clean
	sudo docker build -f scripts/test-centos-7.dockerfile -t me-test-centos-7 .
	sudo docker run --rm me-test-centos-7

.PHONY: debug-centos-7
debug-centos-7: clean
	sudo docker build -f scripts/test-centos-7.dockerfile -t me-test-centos-7 .
	sudo docker run --rm -it me-test-centos-7 /bin/bash

.PHONY: clean
clean:
	cd pooled-jms && make clean
	cd qpid-jms && make clean
	cd qpid-proton-cpp && make clean
	cd qpid-proton-python && make clean
	cd rhea && make clean
	cd vertx-proton && make clean
	find python -name \*.pyc -delete

.PHONY: update-%
update-%:
	curl "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py" -o python/$*.py
