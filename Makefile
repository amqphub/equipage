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

.PHONY: test
test:
	py.test -v --capture=no python/tests.py

.PHONY: clean
clean:
	find python -type f -name \*.pyc -delete
	find . -type d -name __pycache__ -delete

.PHONY: update-plano
update-plano:
	curl "https://raw.githubusercontent.com/ssorj/plano/master/python/plano.py" -o python/plano.py

.PHONY: update-rhea
update-rhea:
	rm -rf node_modules/rhea
	scripts/git-export "git@github.com:grs/rhea.git" master node_modules/rhea
