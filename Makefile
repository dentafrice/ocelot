all: bootstrap test

bootstrap:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r requirements-test.txt

test:
	nosetests
