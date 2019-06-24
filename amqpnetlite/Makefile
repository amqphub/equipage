SOURCES := $(shell find . -type f -name \*.csproj)
BIN_DIRS := ${SOURCES:%.csproj=%/bin}
OBJ_DIRS := ${SOURCES:%.csproj=%/obj}

.PHONY: build
build: ${BIN_DIRS}

.PHONY: clean
clean:
	rm -rf ${BIN_DIRS} ${OBJ_DIRS}

.PHONY:
%/bin:
	dotnet build $(dir $*)
