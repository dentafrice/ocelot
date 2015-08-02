import os

from ocelot import config
from ocelot.tests.test_case import (  # noqa
    DatabaseTestCase,
    fixtures_manager,
    TestCase,
)

ROOT_PATH = os.path.abspath(os.path.dirname(__file__) + '../../../')
FIXTURES_PATH = os.path.join(ROOT_PATH, config.get('testing.fixtures_file'))


def setup_package():
    # Called by nosetests to setup the test suite
    fixtures_manager.load(FIXTURES_PATH, models_package='ocelot.services.datastores')
