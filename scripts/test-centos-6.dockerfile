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

FROM centos:6

RUN yum -q -y update && yum -q clean all

RUN yum -q -y install epel-release

RUN yum -y install gcc-c++ java-1.8.0-openjdk-devel make npm qpid-proton-c-devel qpid-proton-cpp-devel wget

RUN yum -y install nodejs python python-argparse python2-qpid-proton cyrus-sasl-plain cyrus-sasl-md5

RUN wget https://www-us.apache.org/dist/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.tar.gz
RUN tar -xf apache-maven-3.6.1-bin.tar.gz
ENV PATH=/apache-maven-3.6.1/bin:$PATH

# XXX https://bugzilla.redhat.com/show_bug.cgi?id=1562592
RUN npm config set strict-ssl false

RUN npm install -g rhea

COPY . /src

ENV NODE_PATH=/usr/lib/node_modules
WORKDIR /src

RUN make install

# XXX add rhea back in
CMD ["equipage", "test", "pooled-jms", "qpid-jms", "qpid-proton-python", "vertx-proton"]