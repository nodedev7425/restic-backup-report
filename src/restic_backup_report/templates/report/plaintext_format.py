from jinja2 import Template


template: Template = Template("""
Repositories

{% for repository, report in repos.items() %}
    Repository: {{ repository }}
    Report: {{ report }}
{% endfor %}

Storage

{% for storage, report in storages.items() %}
    Storage: {{ storage }}
    Report: {{ report }}
{% endfor %}
""")