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
    engine = engine or get_engine()

    BaseStore.metadata.create_all(engine)


def get_engine(url=None):
    url = url or config.get('external.database.sqlalchemy.url')

    return create_engine(url)


def initialize(engine=None):
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


from ocelot.services.datastores.pipeline import PipelineStore  # noqa
from ocelot.services.datastores.pipeline_schedule import PipelineScheduleStore  # noqa
from ocelot.services.datastores.task import TaskStore  # noqa
from ocelot.services.datastores.task_connection import TaskConnectionStore  # noqa
