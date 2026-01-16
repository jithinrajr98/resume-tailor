"""PDF generation using fpdf2."""

from fpdf import FPDF
from io import BytesIO


class ResumePDF(FPDF):
    """Custom PDF class for resume generation."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_margins(20, 15, 20)

    def add_header(self, name: str, contact: dict):
        """Add name and contact information header."""
        # Name
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, name, ln=True, align="C")

        # Contact line
        contact_parts = []
        if contact.get("email"):
            contact_parts.append(contact["email"])
        if contact.get("phone"):
            contact_parts.append(contact["phone"])
        if contact.get("location"):
            contact_parts.append(contact["location"])
        if contact.get("linkedin"):
            contact_parts.append(contact["linkedin"])
        if contact.get("github"):
            contact_parts.append(contact["github"])

        if contact_parts:
            self.set_font("Helvetica", "", 9)
            contact_line = " | ".join(contact_parts)
            self.cell(0, 5, contact_line, ln=True, align="C")

        self.ln(3)

    def add_section_title(self, title: str):
        """Add a section title with underline."""
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 7, title.upper(), ln=True)
        self.set_draw_color(50, 50, 50)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(2)

    def add_experience(self, experiences: list):
        """Add work experience section."""
        if not experiences:
            return

        self.add_section_title("Experience")

        for exp in experiences:
            # Company and title line
            self.set_font("Helvetica", "B", 10)
            title_company = f"{exp.get('title', '')} | {exp.get('company', '')}"
            self.cell(0, 5, title_company, ln=False)

            # Dates on the right
            self.set_font("Helvetica", "", 9)
            dates = exp.get("dates", "")
            self.cell(0, 5, dates, ln=True, align="R")

            # Location if present
            if exp.get("location"):
                self.set_font("Helvetica", "I", 9)
                self.cell(0, 4, exp["location"], ln=True)

            # Bullet points
            self.set_font("Helvetica", "", 9)
            for bullet in exp.get("bullets", []):
                self.set_x(25)
                self.multi_cell(0, 4, f"* {bullet}")

            self.ln(2)

    def add_education(self, education: list):
        """Add education section."""
        if not education:
            return

        self.add_section_title("Education")

        for edu in education:
            self.set_font("Helvetica", "B", 10)
            degree_field = edu.get("degree", "")
            if edu.get("field"):
                degree_field += f" in {edu['field']}"
            self.cell(0, 5, degree_field, ln=False)

            # Dates on the right
            self.set_font("Helvetica", "", 9)
            dates = edu.get("dates", "")
            self.cell(0, 5, dates, ln=True, align="R")

            # Institution
            self.set_font("Helvetica", "", 9)
            institution = edu.get("institution", "")
            if edu.get("gpa"):
                institution += f" | GPA: {edu['gpa']}"
            self.cell(0, 4, institution, ln=True)

            self.ln(1)

    def add_skills(self, skills: dict):
        """Add skills section."""
        if not skills:
            return

        self.add_section_title("Skills")
        self.set_font("Helvetica", "", 9)

        for category, skill_list in skills.items():
            if skill_list:
                self.set_font("Helvetica", "B", 9)
                label = f"{category}: "
                label_width = self.get_string_width(label) + 2
                self.cell(label_width, 5, label, ln=False)
                self.set_font("Helvetica", "", 9)
                skills_text = ", ".join(skill_list) if isinstance(skill_list, list) else str(skill_list)
                self.multi_cell(0, 5, skills_text)

        self.ln(1)

    def add_summary(self, summary: str):
        """Add professional summary section."""
        if not summary:
            return

        self.add_section_title("Summary")
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 4, summary)
        self.ln(2)

    def add_projects(self, projects: list):
        """Add projects section."""
        if not projects:
            return

        self.add_section_title("Projects")

        for project in projects:
            self.set_font("Helvetica", "B", 10)
            self.cell(0, 5, project.get("name", ""), ln=True)

            if project.get("technologies"):
                self.set_font("Helvetica", "I", 9)
                techs = project["technologies"]
                if isinstance(techs, list):
                    techs = ", ".join(techs)
                self.cell(0, 4, techs, ln=True)

            if project.get("description"):
                self.set_font("Helvetica", "", 9)
                self.multi_cell(0, 4, project["description"])

            for bullet in project.get("bullets", []):
                self.set_font("Helvetica", "", 9)
                self.set_x(25)
                self.multi_cell(0, 4, f"* {bullet}")

            self.ln(1)

    def add_certifications(self, certifications: list):
        """Add certifications section."""
        if not certifications:
            return

        self.add_section_title("Certifications")
        self.set_font("Helvetica", "", 9)

        for cert in certifications:
            cert_text = cert.get("name", "")
            if cert.get("issuer"):
                cert_text += f" - {cert['issuer']}"
            if cert.get("date"):
                cert_text += f" ({cert['date']})"
            self.cell(0, 5, f"* {cert_text}", ln=True)

        self.ln(1)


def generate_pdf(resume_data: dict) -> bytes:
    """
    Generate a PDF from structured resume data.

    Args:
        resume_data: Dictionary containing resume sections.

    Returns:
        PDF as bytes.
    """
    pdf = ResumePDF()

    # Header with name and contact
    pdf.add_header(
        resume_data.get("name", ""),
        resume_data.get("contact", {}),
    )

    # Summary
    pdf.add_summary(resume_data.get("summary", ""))

    # Experience
    pdf.add_experience(resume_data.get("experience", []))

    # Education
    pdf.add_education(resume_data.get("education", []))

    # Skills
    pdf.add_skills(resume_data.get("skills", {}))

    # Projects
    pdf.add_projects(resume_data.get("projects", []))

    # Certifications
    pdf.add_certifications(resume_data.get("certifications", []))

    # Output to bytes
    return bytes(pdf.output())
