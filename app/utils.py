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

class BeautifulCVPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.primary_color = (63, 81, 181)
        self.secondary_color = (25, 118, 210)
        self.accent_color = (255, 193, 7)
        self.text_dark = (33, 33, 33)
        self.text_light = (117, 117, 117)
        self.background_light = (248, 249, 250)

    def header(self):
        self.set_fill_color(*self.background_light)
        self.rect(0, 0, 210, 20, 'F')

    def add_section_header(self, title, icon=""):
        self.ln(8)
        self.set_fill_color(*self.primary_color)
        self.rect(10, self.get_y(), 190, 12, 'F')
        self.set_font('Arial', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, f"{icon} {title}", ln=True, align='L')
        self.set_text_color(*self.text_dark)
        self.ln(3)

    def add_contact_info(self, name, email, phone, address):
        self.set_font('Arial', 'B', 28)
        self.set_text_color(*self.primary_color)
        self.cell(0, 15, name, ln=True, align='C')
        self.ln(5)
        contact_y = self.get_y()
        self.set_fill_color(*self.background_light)
        self.rect(20, contact_y, 170, 35, 'F')

        self.set_font('Arial', '', 10)
        self.set_text_color(*self.text_dark)

        self.set_xy(30, contact_y + 5)
        self.set_font('Arial', 'B', 10)
        self.cell(15, 6, "Email:", ln=0)
        self.set_font('Arial', '', 10)
        self.cell(0, 6, email, ln=True)

        self.set_x(30)
        self.set_font('Arial', 'B', 10)
        self.cell(15, 6, "Phone:", ln=0)
        self.set_font('Arial', '', 10)
        self.cell(0, 6, phone, ln=True)

        self.set_x(30)
        self.set_font('Arial', 'B', 10)
        self.cell(15, 6, "Address:", ln=0)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, " " + address)

        self.ln(10)

    def add_content_section(self, title, content, icon=" "):
        if not content or content.strip() == "":
            return
        self.add_section_header(title, icon)
        self.set_font('Arial', '', 11)
        self.set_text_color(*self.text_dark)

        lines = content.split('\n')
        for line in lines:
            if line.strip():
                self.set_x(15)
                self.multi_cell(180, 6, line.strip())
                self.ln(2)

    def add_skills_section(self, skills):
        if not skills or skills.strip() == "":
            return

        self.add_section_header("Skills & Expertise", " ")
        skill_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
        self.set_font('Arial', '', 10)
        self.set_text_color(*self.text_dark)

        x_start = 15
        y_start = self.get_y()
        col_width = 85

        for i, skill in enumerate(skill_list):
            if i % 2 == 0:
                x = x_start
                if i > 0:
                    y_start += 8
                y = y_start
            else:
                x = x_start + col_width
                y = y_start

            self.set_xy(x, y)
            self.set_text_color(*self.secondary_color)
            self.cell(3, 6, "-", ln=0)

            self.set_x(x + 5)
            self.set_text_color(*self.text_dark)
            self.cell(col_width - 5, 6, skill)

        self.ln(15)

    def add_footer_decoration(self):
        self.ln(10)
        footer_y = self.get_y()
        self.set_draw_color(*self.accent_color)
        self.set_line_width(2)
        self.line(20, footer_y, 190, footer_y)

        self.ln(5)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(*self.text_light)
        self.cell(0, 5, "Generated with Careerly - Professional CV Builder", ln=True, align='C')

def generate_cv_pdf(user):
    # Include address in the template to allow SSTI evaluation
    cv_template = """
Name: {{ name }} Email: {{ email }}
Phone: {{ phone }}
Address: {{ address }}
About {{name}}: {{ bio }}
Experience: {{ experience }}
Skills: {{ skills }}
"""

    env = Environment()
    env.filters['ssti_sanitize'] = ssti_sanitize
    env.globals.update(os=os, uuid=uuid)

    template = env.from_string(cv_template)

    # Only sanitize the other fields, leave address raw to be vulnerable
    safe_name = ssti_sanitize(user.name)
    safe_email = ssti_sanitize(user.email)
    safe_phone = ssti_sanitize(user.phone)

    # unsafe_address = unfiltered user input (vulnerable to SSTI)
    unsafe_address = user.address

    # First render evaluates all safe fields and injects raw SSTI payload in address
    first_render = template.render(
        name=safe_name,
        email=safe_email,
        phone=safe_phone,
        address=unsafe_address,
        bio=user.bio,
        experience=user.experience,
        skills=user.skills
    )

    # Second render evaluates the SSTI inside address field
    second_template = env.from_string(first_render)
    rendered_cv = second_template.render()

    # Now extract final rendered fields for PDF
    name = safe_name
    email = safe_email
    phone = safe_phone
    address = None

    content_sections = {}
    current_section = None

    for line in rendered_cv.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("Name:"):
            name = line.split(":", 1)[1].strip().split("Email")[0].strip()
        elif line.startswith("Email:"):
            email = line.split(":", 1)[1].strip()
        elif line.startswith("Phone:"):
            phone = line.split(":", 1)[1].strip()
        elif line.startswith("Address:"):
            address = line.split(":", 1)[1].strip()
        elif line.startswith('About '):
            current_section = 'About Me'
            content_sections[current_section] = line.split(':', 1)[1].strip()
        elif line.startswith('Experience:'):
            current_section = 'Professional Experience'
            content_sections[current_section] = line.split(':', 1)[1].strip()
        elif line.startswith('Skills:'):
            current_section = 'Skills'
            content_sections[current_section] = line.split(':', 1)[1].strip()
        elif current_section:
            content_sections[current_section] += '\n' + line

    pdf = BeautifulCVPDF()
    pdf.add_page()
    pdf.add_contact_info(name, email, phone, address)

    section_order = [
        ('About Me', ' '),
        ('Professional Experience', ' ')
    ]

    for section_name, icon in section_order:
        if section_name in content_sections:
            pdf.add_content_section(section_name, content_sections[section_name], icon)

    if 'Skills' in content_sections:
        pdf.add_skills_section(content_sections['Skills'])

    pdf.add_footer_decoration()

    temp_dir = tempfile.gettempdir()
    random_filename = f"{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join(temp_dir, random_filename)
    pdf.output(pdf_path)

    return pdf_path