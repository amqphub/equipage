CCFLAGS := -Os -std=c++11 -lstdc++
TARGETS := request respond

.PHONY: build
build: ${TARGETS}

.PHONY: clean
clean:
	rm -f ${TARGETS}

%: %.cpp
	${CXX} $< -o $@ ${CCFLAGS} -lqpid-proton -lqpid-proton-cpp
