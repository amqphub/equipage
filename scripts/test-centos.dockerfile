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

FROM centos

RUN yum -q -y update && yum -q clean all

RUN yum -q -y install epel-release

RUN yum -q -y install gcc-c++ java-1.8.0-openjdk-devel make maven nodejs npm ruby cyrus-sasl-plain cyrus-sasl-md5

RUN yum -y install python3-qpid-proton qpid-proton-c-devel qpid-proton-cpp-devel rubygem-qpid_proton

RUN ln -snf /usr/bin/python3 /usr/bin/python

# RUN alternatives --set python /usr/bin/python3

# RUN rpm -Uvh https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm && yum -q -y update && yum -y install dotnet-sdk-3.1

RUN npm install -g rhea

COPY . /src

ENV NODE_PATH=/usr/lib/node_modules
WORKDIR /src

RUN make install

# Missing: dotnet ruby
CMD ["equipage", "test", "pooled-jms", "qpid-jms", "qpid-proton-cpp", "qpid-proton-python", "rhea", "vertx-proton"]
