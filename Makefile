export PYTHONPATH := ${CURDIR}/python
export NODE_PATH := ${CURDIR}/rhea/node_modules

.PHONY: build
build:
	cd pooled-jms && make build
	cd qpid-jms && make build
	cd qpid-proton-cpp && make build
	cd qpid-proton-python && make build
	cd rhea && make build

.PHONY: test
test: build
	scripts/run-tests --timeout 10

.PHONY: clean
clean:
	cd pooled-jms && make clean
	cd qpid-jms && make clean
	cd qpid-proton-cpp && make clean
	cd qpid-proton-python && make clean
	cd rhea && make clean
	find python -name \*.pyc -delete

.PHONY: update-%
update-%:
	curl "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py" -o python/$*.py
