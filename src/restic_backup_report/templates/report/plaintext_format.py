from jinja2 import Template


template: Template = Template("""
{% for repository, report in data.items() %}
    Repository: {{ repository }}
    Report: {{ report }}
{% endfor %}
""")