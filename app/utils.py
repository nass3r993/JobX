import re
from jinja2 import Environment
import tempfile
import os
import uuid
from fpdf import FPDF
from flask import current_app

def ssti_sanitize(value):
    if not isinstance(value, str):
        return value
    value = re.sub(r'{{', '&#123;&#123;', value)
    value = re.sub(r'}}', '&#125;&#125;', value)
    value = re.sub(r'{%', '&#123;% ', value)
    value = re.sub(r'%}', ' %&#125;', value)
    value = re.sub(r'{#', '&#123;#', value)
    value = re.sub(r'#}', '#&#125;', value)
    return value

def generate_cv_pdf(user):
    cv_template = """
Name: {{ name }}
Email: {{ email }}
Phone: {{ phone }}
Address: {{ address | safe }}
"""

    env = Environment()
    env.filters['ssti_sanitize'] = ssti_sanitize

    # Only expose os to SSTI payloads, NOT config
    env.globals.update(os=os)

    template = env.from_string(cv_template)

    safe_name = ssti_sanitize(user.name)
    safe_email = ssti_sanitize(user.email)
    safe_phone = ssti_sanitize(user.phone)

    first_render = template.render(
        name=safe_name,
        email=safe_email,
        phone=safe_phone,
        address=user.address,  # vulnerable SSTI
    )

    second_template = env.from_string(first_render)
    rendered_cv = second_template.render()

    # Start generating PDF
    pdf = FPDF()
    pdf.add_page()

    # Add title
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(99, 102, 241)  # Indigo shade
    pdf.cell(0, 15, "JobX CV", ln=True, align='C')
    pdf.ln(10)  # spacing after title

    # Reset font for content
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)  # black text

    # Format each line with bold label and normal text
    for line in rendered_cv.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(40, 10, f"{key.strip()}: ", ln=0)
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, value.strip())
        else:
            pdf.multi_cell(0, 10, line)

    # Save the PDF to a temporary file
    temp_dir = tempfile.gettempdir()
    random_filename = f"{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join(temp_dir, random_filename)
    pdf.output(pdf_path)

    return pdf_path
