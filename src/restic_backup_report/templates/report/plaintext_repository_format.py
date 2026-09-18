from jinja2 import Template


template: Template = Template("""
{% for repository in repositories %}
    {{ repository }}
{% endfor %}
""")