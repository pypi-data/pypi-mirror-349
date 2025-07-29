from jinja2 import Template
import os

def generate_html_report(context, output_file):
    template_path = os.path.join(os.path.dirname(__file__), 'report_template.html')

    with open(template_path, 'r') as f:
        html_template = f.read()

    template = Template(html_template)
    rendered = template.render(**context)

    with open(output_file, 'w') as f:
        f.write(rendered)
