from jinja2 import Template


template: Template = Template("""
name: {{ storage_name | tojson }}
path: {{ storage_path | tojson }}
warning_percent: {{ storage_warning_percent }}
critical_percent: {{ storage_critical_percent }}
""")