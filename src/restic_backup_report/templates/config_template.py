from jinja2 import Template

template = Template("""
version: {{ config_standard }}

secrets:
    checksum: {{ master_key_checksum }}
    salt: {{ master_key_checksum_salt }}
""")