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

scheduler:
	python -m 'ocelot.scheduler'

seed:
	psql template1 -c 'drop database if exists ocelot;'
	psql template1 -c 'create database ocelot;'
	OCELOT_CONFIG=config/development.yaml python -m 'ocelot.scripts.seed'

test: unit_tests lint

unit_tests:
	psql template1 -c 'drop database if exists ocelot_test;'
	psql template1 -c 'create database ocelot_test;'
	nosetests
