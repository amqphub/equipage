export PYTHONPATH := ${PWD}/python
export NODE_PATH := ${PWD}/rhea/node_modules

.PHONY: build
build:
	cd qpid-jms && make build
	cd qpid-proton-cpp && make build
	cd qpid-proton-python && make build
	cd rhea && make build

.PHONY: test
test: build
	scripts/run-tests --timeout 10

.PHONY: clean
clean:
	cd qpid-jms && make clean
	cd qpid-proton-cpp && make clean
	cd qpid-proton-python && make clean
	cd rhea && make clean
	find python -name \*.pyc -delete

.PHONY: update-%
update-%:
	curl "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py" -o python/$*.py
