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

FROM quay.io/centos/centos:7

RUN yum -q -y update && yum -q clean all

RUN yum -q -y install epel-release

RUN yum -q -y install gcc-c++ java-1.8.0-openjdk-devel make maven nodejs npm ruby cyrus-sasl-plain cyrus-sasl-md5

RUN rpm -Uvh https://packages.microsoft.com/config/centos/7/packages-microsoft-prod.rpm

RUN yum -y install python2-qpid-proton qpid-proton-c-devel qpid-proton-cpp-devel rubygem-qpid_proton dotnet-sdk-5.0

RUN npm install -g rhea

COPY . /src

ENV NODE_PATH=/usr/lib/node_modules
WORKDIR /src

RUN make install

CMD ["equipage", "test"]
