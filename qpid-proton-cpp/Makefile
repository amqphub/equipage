CCFLAGS := -Os -std=c++11 -lstdc++ -lpthread -lqpid-proton-cpp
SOURCES := $(shell find . -name \*.cpp)
TARGETS := ${SOURCES:./%.cpp=build/%}

.PHONY: build
build: ${TARGETS}

.PHONY: clean
clean:
	rm -rf build

build/%: %.cpp
	@mkdir -p ${@D}
	${CXX} $< -o $@ ${CCFLAGS}
