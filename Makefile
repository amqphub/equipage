#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

.NOTPARALLEL:

DESTDIR := ""
PREFIX := /usr/local
INSTALLED_QEXAMPLES_HOME = ${PREFIX}/share/qexamples

export QEXAMPLES_HOME := ${CURDIR}/build/qexamples
export PATH := ${CURDIR}/build/bin:${PATH}
export PYTHONPATH := ${QEXAMPLES_HOME}/python:${CURDIR}/python

BIN_SOURCES := $(shell find bin -type f -name \*.in)
BIN_TARGETS := ${BIN_SOURCES:%.in=build/%}

PYTHON_SOURCES := $(shell find python -type f -name \*.py)
PYTHON_TARGETS := ${PYTHON_SOURCES:%=build/qexamples/%}

EXAMPLE_DIRS := pooled-jms qpid-jms qpid-proton-cpp qpid-proton-python qpid-proton-ruby rhea vertx-proton
EXAMPLE_SOURCES := $(shell find ${EXAMPLE_DIRS})
EXAMPLE_TARGETS := ${EXAMPLE_SOURCES:%=build/qexamples/%}

.PHONY: default
default: build

.PHONY: help
help:
	@echo "build          Build the code"
	@echo "install        Install the code"
	@echo "clean          Clean up the source tree"
	@echo "test           Run the tests"

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	find python -type d -name __pycache__ -delete
	rm -rf build

.PHONY: build
build: ${BIN_TARGETS} ${PYTHON_TARGETS} ${EXAMPLE_TARGETS} build/prefix.txt
	scripts/smoke-test

.PHONY: install
install:
	scripts/install-files build/bin ${DESTDIR}$$(cat build/prefix.txt)/bin
	scripts/install-files build/qexamples ${DESTDIR}$$(cat build/prefix.txt)/share/qexamples

.PHONY: test
test: build
	qexamples build
	qexamples-test

.PHONY: big-test
big-test: test test-centos-7 test-fedora test-ubuntu

.PHONY: test-centos-7
test-centos-7: clean
	sudo docker build -f scripts/test-centos-7.dockerfile -t me-test-centos-7 .
	sudo docker run --rm me-test-centos-7

.PHONY: debug-centos-7
debug-centos-7: clean
	sudo docker build -f scripts/test-centos-7.dockerfile -t me-test-centos-7 .
	sudo docker run --rm -it me-test-centos-7 /bin/bash

.PHONY: test-fedora
test-fedora: clean
	sudo docker build -f scripts/test-fedora.dockerfile -t me-test-fedora .
	sudo docker run --rm me-test-fedora

.PHONY: debug-fedora
debug-fedora: clean
	sudo docker build -f scripts/test-fedora.dockerfile -t me-test-fedora .
	sudo docker run --rm -it me-test-fedora /bin/bash

.PHONY: test-ubuntu
test-ubuntu: clean
	sudo docker build -f scripts/test-ubuntu.dockerfile -t me-test-ubuntu .
	sudo docker run --rm me-test-ubuntu

.PHONY: debug-ubuntu
debug-ubuntu: clean
	sudo docker build -f scripts/test-ubuntu.dockerfile -t me-test-ubuntu .
	sudo docker run --rm -it me-test-ubuntu /bin/bash

build/prefix.txt:
	echo ${PREFIX} > build/prefix.txt

build/bin/%: bin/%.in
	scripts/configure-file -a qexamples_home=${INSTALLED_QEXAMPLES_HOME} $< $@

build/qexamples/python/qexamples/%: python/qexamples/% python/brokerlib.py python/commandant.py python/plano.py
	@mkdir -p ${@D}
	cp $< $@

build/qexamples/%: %
	@mkdir -p ${@D}
	cp -r $< $@

.PHONY: update-%
update-%:
	curl "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py" -o python/$*.py

# .PHONY: clean
# clean:
#	cd pooled-jms && make clean
#	cd qpid-jms && make clean
#	cd qpid-proton-cpp && make clean
#	cd qpid-proton-python && make clean
#	cd rhea && make clean
#	cd vertx-proton && make clean
#	find python -name \*.pyc -delete
