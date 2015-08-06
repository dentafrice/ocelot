from ocelot.pipeline.tasks.operations.dict.base_dict_operation import BaseDictOperation


class DictFilterOperation(BaseDictOperation):
    def _allow_item(self, item):
        """Only return items that match.

        :param dict item:
        :returns boolean:
        """
        return bool(item)

    def _perform_operation(self, item):
        """Validates that the item matches all/any the configured rules.

        :param dict item:
        :returns item:
        """
        matches = [
            self._does_item_match_rule(item, rule)
            for rule in self.config.get('rules')
        ]

        if self.config['type'] == 'all':
            if not all(matches):
                return
        elif self.config['type'] == 'any':
            if not any(matches):
                return

            if not self._does_item_match_rule(item, rule):
                return

        return item

    def _does_item_match_rule(self, item, rule):
        """Returns whether or not an item matches a rule.

        :param dict item:
        :param dict rule:
            type
            path
            value
        :returns boolean:
        """
        if rule['type'] == 'equals':
            matches = self._get_matches_for_path(item, rule['path'])

            if not matches:
                return False

            for match in matches:
                if not match.value == rule['value']:
                    return False

        return True
