from jinja2 import Template

template: Template = Template("""
name: {{ target_name }}
type: {{ target_type }}
format: {{ target_format }}
{{ format_type }}:
""")