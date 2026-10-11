from jinja2 import Template


template: Template = Template("""
name: {{ repository_name | tojson }}
display_name: {{ repository_display_name | tojson }}
path: {{ repository_path | tojson }}
password: {{ repository_password | tojson }}
password_nonce: {{ repository_password_nonce | tojson }}
report: {{ report_interval | tojson }}
backup:
  frequency: {{ backup_frequency | tojson }}
  tolerance: {{ backup_tolerance }}
""")