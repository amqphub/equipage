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
INSTALLED_EQUIPAGE_HOME = ${PREFIX}/share/equipage
PYTHON_EXECUTABLE := /usr/bin/python

export EQUIPAGE_HOME := ${CURDIR}/build/equipage
export PATH := ${CURDIR}/build/bin:${PATH}
export PYTHONPATH := ${EQUIPAGE_HOME}/python:${CURDIR}/python

BIN_SOURCES := $(shell find bin -type f -name \*.in)
BIN_TARGETS := ${BIN_SOURCES:%.in=build/%}

PYTHON_SOURCES := $(shell find python -type f -name \*.py)
PYTHON_TARGETS := ${PYTHON_SOURCES:%=build/equipage/%}

EXAMPLE_DIRS := amqpnetlite pooled-jms qpid-jms qpid-proton-cpp qpid-proton-python qpid-proton-ruby rhea vertx-proton
EXAMPLE_SOURCES := $(shell find ${EXAMPLE_DIRS})
EXAMPLE_TARGETS := ${EXAMPLE_SOURCES:%=build/equipage/%}

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
install: build
	scripts/install-files build/bin ${DESTDIR}$$(cat build/prefix.txt)/bin
	scripts/install-files build/equipage ${DESTDIR}$$(cat build/prefix.txt)/share/equipage

.PHONY: test
test: build
	equipage test

.PHONY: big-test
big-test: test test-centos-7 test-fedora test-ubuntu

.PHONY: test-centos-6
test-centos-6: clean
	sudo docker build -f scripts/test-centos-6.dockerfile -t equipage-test-centos-6 .
	sudo docker run --rm equipage-test-centos-6

.PHONY: debug-centos-6
debug-centos-6: clean
	sudo docker build -f scripts/test-centos-6.dockerfile -t equipage-test-centos-6 .
	sudo docker run --rm -it equipage-test-centos-6 /bin/bash

.PHONY: test-centos-7
test-centos-7: clean
	sudo docker build -f scripts/test-centos-7.dockerfile -t equipage-test-centos-7 .
	sudo docker run --rm equipage-test-centos-7

.PHONY: debug-centos-7
debug-centos-7: clean
	sudo docker build -f scripts/test-centos-7.dockerfile -t equipage-test-centos-7 .
	sudo docker run --rm -it equipage-test-centos-7 /bin/bash

.PHONY: test-fedora
test-fedora: clean
	sudo docker build -f scripts/test-fedora.dockerfile -t equipage-test-fedora .
	sudo docker run --rm equipage-test-fedora

.PHONY: debug-fedora
debug-fedora: clean
	sudo docker build -f scripts/test-fedora.dockerfile -t equipage-test-fedora .
	sudo docker run --rm -it equipage-test-fedora /bin/bash

.PHONY: test-ubuntu
test-ubuntu: clean
	sudo docker build -f scripts/test-ubuntu.dockerfile -t equipage-test-ubuntu .
	sudo docker run --rm equipage-test-ubuntu

.PHONY: debug-ubuntu
debug-ubuntu: clean
	sudo docker build -f scripts/test-ubuntu.dockerfile -t equipage-test-ubuntu .
	sudo docker run --rm -it equipage-test-ubuntu /bin/bash

build/prefix.txt:
	echo ${PREFIX} > build/prefix.txt

build/bin/%: bin/%.in
	scripts/configure-file -a equipage_home=${INSTALLED_EQUIPAGE_HOME} -a python_executable=${PYTHON_EXECUTABLE} $< $@

build/equipage/python/equipage/%: python/equipage/% python/brokerlib.py python/commandant.py python/plano.py
	@mkdir -p ${@D}
	cp $< $@

build/equipage/%: %
	@mkdir -p ${@D}
	cp -Tr $< $@

.PHONY: update-brokerlib
update-brokerlib:
	curl -sfo python/brokerlib.py "https://raw.githubusercontent.com/ssorj/qtools/master/python/brokerlib.py"

.PHONY: update-%
update-%:
	curl -sfo python/$*.py "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py"
