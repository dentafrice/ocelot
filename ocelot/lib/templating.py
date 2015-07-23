from jinja2 import Environment, DictLoader

FAKE_TEMPLATE_NAME = 'fake_template_name'


def render_template(template_value, template_variables=None):
    """Render a Jinja2 template.

    :param str template_value: Jinja2 template string
    :param dict template_variables: variables to include in template.
    """
    template_environment = Environment(loader=DictLoader({
        FAKE_TEMPLATE_NAME: template_value,
    }))

    jinja_template = template_environment.get_template(FAKE_TEMPLATE_NAME)

    return jinja_template.render(template_variables or {})
