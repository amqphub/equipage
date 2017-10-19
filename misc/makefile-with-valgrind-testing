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

CCFLAGS := -Wall -Os -std=c++11 -lstdc++
TARGETS := client

# .PHONY: test
# test: build
# 	./multithreaded-client amqp://localhost q0 1000

# .PHONY: big-test
# big-test:
# 	set -e; for i in {1..100}; do ./multithreaded-client amqp://localhost q0 1000; done

# .PHONY: test-with-memcheck
# test-with-memcheck:
# 	valgrind ./multithreaded-client amqp://localhost q0 1000

# .PHONY: test-with-helgrind
# test-with-helgrind:
# 	valgrind --tool=helgrind ./multithreaded-client amqp://localhost q0 100

.PHONY: build
build: ${TARGETS}

.PHONY: clean
clean:
	rm -f ${TARGETS}

%: %.cpp
	${CXX} $< -o $@ ${CCFLAGS} -lqpid-proton -lqpid-proton-cpp -lpthread
