DESTDIR := ""
PREFIX := ${HOME}/.local
home = ${PREFIX}/share/qpid-examples

export PYTHONPATH := ${PWD}/python
export NODE_PATH := ${PWD}/node_modules:/usr/lib/node_modules:/usr/local/lib/node_modules

.PHONY: build
build:
	mkdir -p build/jms
	cd jms && mvn package
	mv jms/target build/jms/target

# .PHONY: test
# test:
# 	py.test -v --capture=no python/tests.py

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	find . -type d -name __pycache__ -delete

# .PHONY: docker-build
# docker-build:
# 	sudo docker build -t ssorj/messaging-examples .

# .PHONY: docker-run
# docker-run:
# 	sudo docker run -it ssorj/messaging-examples

# .PHONY: docker-push
# docker-push:
# 	sudo docker push ssorj/messaging-examples

.PHONY: update-%
update-%:
	curl "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py" -o python/$*.py
