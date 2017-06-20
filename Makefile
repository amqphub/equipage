.PHONY: test
test:
	cd cpp && ./test.sh
	cd javascript && ./test.sh
	cd python && ./test.sh
