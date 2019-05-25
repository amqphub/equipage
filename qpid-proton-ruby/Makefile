.PHONY: build
build:

.PHONY: test
test: build
	cd .. && PYTHONPATH=$$PWD/python scripts/test test_qpid_proton_ruby\*

.PHONY: clean
clean:
