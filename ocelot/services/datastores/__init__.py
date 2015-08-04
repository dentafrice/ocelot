import uuid

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound  # noqa
from sqlalchemy.types import TypeDecorator, CHAR

from ocelot import config


BaseStore = declarative_base()
Session = scoped_session(sessionmaker())


def create_tables(engine=None):
    """Creates all tables based on the defined metadata.

    :param Engine engine: (optional)
    """
    engine = engine or get_engine()

    BaseStore.metadata.create_all(engine)


def get_engine(url=None):
    """Returns Engine for a URL.

    If URL is not provided it will be fetched from the configuration.

    :param str url: (optional)
    :returns Engine:
    """
    url = url or config.get('external.database.sqlalchemy.url')

    return create_engine(url)


def initialize(engine=None):
    """Binds session and metadata to engine.

    :param Engine engine: (optional)
    """
    engine = engine or get_engine()

    Session.configure(bind=engine)
    BaseStore.metadata.bind = engine


class GUID(TypeDecorator):
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return unicode(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


# Import all datastores here so that they can be created correctly.
# maybe move this to configuration and import it dynamically?
from ocelot.services.datastores.pipeline import PipelineStore  # noqa
from ocelot.services.datastores.pipeline_schedule import PipelineScheduleStore  # noqa
from ocelot.services.datastores.task import TaskStore  # noqa
from ocelot.services.datastores.task_connection import TaskConnectionStore  # noqa
