from ocelot.pipeline.tasks.operations.dict.dict_filter_operation import DictFilterOperation
from ocelot.tests import DatabaseTestCase


class TestDictFilterOperation(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('fake_dict')

    def test_any_rule_pass(self):
        """Test that when set to `any`, if any rule passes that
        the item is returned."""
        operation = DictFilterOperation(
            config={
                'type': 'any',
                'rules': [
                    {
                        'type': 'equals',
                        'path': '$.level.deep.value',
                        'value': 'no way',
                    },

                    {
                        'type': 'equals',
                        'path': '$.level.deep.value',
                        'value': 'hey',
                    }
                ]
            }
        )

        self.assertEquals(
            operation.process(self.fake_dict),
            self.fake_dict,
        )

    def test_any_rule_fail(self):
        """Test that when set to `any`, if no rules pass that the item
        is returned."""
        operation = DictFilterOperation(
            config={
                'type': 'any',
                'rules': [
                    {
                        'type': 'equals',
                        'path': '$.level.deep.value',
                        'value': 'no way',
                    },

                    {
                        'type': 'equals',
                        'path': '$.level.deep.value',
                        'value': 'still no',
                    }
                ]
            }
        )

        self.assertEquals(
            operation.process(self.fake_dict),
            None,
        )

    def test_all_rules_pass(self):
        """Test that when set to `all`, if all rules pass
        that the item is returned."""
        operation = DictFilterOperation(
            config={
                'type': 'all',
                'rules': [
                    {
                        'type': 'equals',
                        'path': '$.level.array[0].name',
                        'value': 'item1',
                    },

                    {
                        'type': 'equals',
                        'path': '$.level.deep.value',
                        'value': 'hey',
                    }
                ]
            }
        )

        self.assertEquals(
            operation.process(self.fake_dict),
            self.fake_dict,
        )

    def test_all_rules_fail(self):
        """Test that when set to `all`, if only some rules pass that the
        item is not returned."""
        operation = DictFilterOperation(
            config={
                'type': 'all',
                'rules': [
                    {
                        'type': 'equals',
                        'path': '$.level.array[1].name',
                        'value': 'item1',
                    },

                    {
                        'type': 'equals',
                        'path': '$.level.deep.value',
                        'value': 'hey',
                    }
                ]
            }
        )

        operation.process(self.fake_dict)

        self.assertEquals(
            operation.process(self.fake_dict),
            None,
        )
