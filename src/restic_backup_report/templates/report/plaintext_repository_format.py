from jinja2 import Template


template: Template = Template("""{{ repository_display_name }}
name: {{ repository_name }}
""")