FROM fedora
MAINTAINER Justin Ross <jross@apache.org>

RUN dnf -y update && dnf clean all

RUN dnf -y install gcc-c++ git npm python-qpid-proton qpid-proton-cpp-devel && dnf clean all

RUN cd /root && git clone https://github.com/ssorj/messaging-examples

CMD ["/bin/bash"]
