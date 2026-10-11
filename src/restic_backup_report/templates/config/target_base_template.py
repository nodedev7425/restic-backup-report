from jinja2 import Template


template: Template = Template("""
name: {{ target_name | tojson }}
type: {{ target_type | tojson }}
format: {{ target_format | tojson }}
config: {}
""")