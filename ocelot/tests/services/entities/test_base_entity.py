import uuid

from schematics.types import UUIDType

from ocelot.services.entities.base_entity import BaseEntity
from ocelot.tests import TestCase


FAKE_UUID = '46cd3346-6be0-456b-8b8f-c9fc1380354f'


class FakeEntity(BaseEntity):
    id = UUIDType()


class TestBaseEntity(TestCase):
    def test_coerce_set(self):
        """Test that values are coerced to native when being set."""
        entity = FakeEntity()

        self.assertIsNone(entity.id)

        entity.id = FAKE_UUID

        self.assertEquals(
            entity.id,
            uuid.UUID(FAKE_UUID),
        )
