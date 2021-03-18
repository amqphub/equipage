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

FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update && apt-get -qq dist-upgrade

RUN apt-get -qq update \
    && apt-get -qq install software-properties-common \
    && add-apt-repository -y ppa:qpid/released \
    && apt-get -qq update \
    && apt-get -qq install build-essential make openjdk-11-jdk maven nodejs python3 ruby npm

RUN apt-get -qq install \
        libqpid-proton-cpp12-dev python3-qpid-proton \
        libsasl2-2 libsasl2-dev libsasl2-modules sasl2-bin

RUN npm install -g rhea

COPY . /src

ENV NODE_PATH=/usr/local/lib/node_modules
WORKDIR /src

RUN make install PYTHON_EXECUTABLE=/usr/bin/python3

# Missing: ruby
CMD ["equipage", "test", "pooled-jms", "qpid-jms", "qpid-proton-cpp", "qpid-proton-python", "rhea", "vertx-proton"]
