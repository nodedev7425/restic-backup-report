from jinja2 import Template

template: Template = Template("""
  - name: {{ repository_name }}
    path: {{ repository_path }}
    password: {{ repository_password }}
    report: {{ report_interval }}
    backup:
      frequency: {{ backup_frequency }}
      tolerance: {{ backup_tolerance }}
""")