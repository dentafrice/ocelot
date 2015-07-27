from schematics.models import Model


class BaseEntity(Model):
    def __setattr__(self, name, value):
        """Hook to coerce values to native when setting attributes."""
        if name[0] != '_':
            value = self._coerce(name, value)

        super(BaseEntity, self).__setattr__(name, value)

    def _coerce(self, name, value):
        """Coerce value to native."""
        if value is not None:
            value = self._fields[name].to_native(value)

        return value
