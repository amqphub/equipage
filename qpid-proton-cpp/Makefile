CCFLAGS := -Os -std=c++11 -lstdc++ -lpthread -lqpid-proton-cpp
SOURCES := $(shell find . -name \*.cpp)
TARGETS := ${SOURCES:./%.cpp=build/%}

.PHONY: build
build: ${TARGETS}

.PHONY: test
test: build
	cd .. && PYTHONPATH=$$PWD/python scripts/test test_qpid_proton_cpp\*

.PHONY: clean
clean:
	rm -rf build

build/%: %.cpp
	@mkdir -p ${@D}
	${CXX} $< -o $@ ${CCFLAGS}
