CCFLAGS := -Os -std=c++11 -lstdc++ -lpthread -lqpid-proton-cpp
SOURCES := $(shell find . -name \*.cpp)
TARGETS := ${SOURCES:./%.cpp=build/%}

.PHONY: build
build: ${TARGETS}

.PHONY: clean
clean:
	rm -rf build

#build/threading/client-03: threading/client-03.cpp
#	@mkdir -p ${@D}
#	${CXX} $< -o $@ -Os -std=c++03 -lpthread -lqpid-proton-cpp

build/%: %.cpp
	@mkdir -p ${@D}
	${CXX} $< -o $@ ${CCFLAGS}
