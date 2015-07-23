from ocelot.lib import templating
from ocelot.tests import TestCase


class TestTemplating(TestCase):
    def test_render_template(self):
        """Test that we can render a template with template variables."""
        fake_template = 'hello there {{user.first_name}} {{top}}'
        fake_variables = {
            'user': {
                'first_name': 'Caleb',
            },

            'top': 'sup',
        }

        rendered_template = templating.render_template(
            fake_template,
            fake_variables,
        )

        self.assertEquals(
            rendered_template,
            'hello there Caleb sup',
        )
