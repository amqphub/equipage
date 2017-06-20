.PHONY: test
test:
	cd qpid-proton-cpp && ./test.sh
	cd qpid-proton-python && ./test.sh
	cd rhea && ./test.sh
