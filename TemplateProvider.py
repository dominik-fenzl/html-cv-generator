from jinja2 import Template


def get_template():
    with open('template.html', 'r') as f:
        template = Template(f.read())

    return template

