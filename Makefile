all: clean bootstrap test

bootstrap:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r requirements-test.txt

clean:
	find . -name '*.pyc' -delete

demo:
	OCELOT_CONFIG=config/development.yaml python -m 'ocelot.main'

lint:
	flake8 ocelot

seed:
	OCELOT_CONFIG=config/development.yaml python -m 'ocelot.scripts.seed'

test: unit_tests lint

unit_tests:
	psql -c 'drop database if exists ocelot_test;'
	psql -c 'create database ocelot_test;'
	nosetests
