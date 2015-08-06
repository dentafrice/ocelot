from ocelot.pipeline.tasks.operations.dict_operation import (
    DictCreateOperation,
)
from ocelot.tests import TestCase


class TestDictCreateOperation(TestCase):
    def test_creates_dict(self):
        """Test that a dict is returned with the provided key => item."""
        create = DictCreateOperation(
            config={
                'key': 'fake_key',
            }
        )

        self.assertEquals(
            create.process('hello there'),
            {
                'fake_key': 'hello there',
            },
        )
