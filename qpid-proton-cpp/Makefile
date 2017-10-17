CCFLAGS := -Os -std=c++11 -lstdc++
TARGETS := send request respond

.PHONY: build
build: ${TARGETS}

.PHONY: clean
clean:
	rm -f ${TARGETS}

%: %.cpp
	${CXX} $< -o $@ ${CCFLAGS} -lqpid-proton -lqpid-proton-cpp
