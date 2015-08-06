from ocelot.pipeline.tasks.operations.dict.base_dict_operation import BaseDictOperation


class DictCreateOperation(BaseDictOperation):
    def _perform_operation(self, item):
        """Creates and returns a new dict.

        The dict will contain one item with the key that
        is provided in the config, and the value passed to the operation.

        Example:
            ```
            operation = DictCreateOperation(
                config={
                    'key': 'fake-key',
                }
            )
            ```

            `operation.process('some-thing')` will return:
            ```
            {
                'fake-key': 'some-thing'
            }
            ```

        :param object item:
        :returns dict: constructed dict with key => item.
        """
        return {
            self.config['key']: item,
        }
