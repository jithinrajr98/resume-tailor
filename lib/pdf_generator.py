"""PDF generation using fpdf2."""

from fpdf import FPDF


class ResumePDF(FPDF):
    """Custom PDF class for resume generation."""

    # Bullet character (using dash for Helvetica compatibility)
    BULLET = "-"

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_margins(18, 15, 18)

    def _add_bullet_point(self, text: str, indent: int = 23, bullet: str = "-"):
        """Add a bullet point with proper text alignment for wrapped lines."""
        # Save current left margin
        original_left_margin = self.l_margin

        # Calculate text start position (after bullet)
        bullet_text = f"{bullet}  "
        self.set_font("Helvetica", "", 10)
        bullet_width = self.get_string_width(bullet_text)
        text_start = indent + bullet_width

        # Print bullet at indent position
        self.set_x(indent)
        self.cell(bullet_width, 5, bullet_text, ln=False)

        # Set left margin so wrapped lines align with text start
        self.set_left_margin(text_start)

        # Print text (will wrap at new left margin)
        self.multi_cell(0, 5, text, align="J")

        # Restore original left margin
        self.set_left_margin(original_left_margin)

    def add_header(self, name: str, contact: dict, title: str = ""):
        """Add name and contact information header."""
        # Name - Times Bold, ALL CAPS, centered
        self.set_font("Times", "B", 24)
        self.cell(0, 12, name.upper(), ln=True, align="C")
        self.ln(2)

        # Contact line: Title | Location | Phone | Email (bold, centered)
        contact_parts = []
        if title:
            contact_parts.append(title)
        if contact.get("location"):
            contact_parts.append(contact["location"])
        if contact.get("phone"):
            contact_parts.append(contact["phone"])
        if contact.get("email"):
            contact_parts.append(contact["email"])

        if contact_parts:
            self.set_font("Helvetica", "B", 10)
            contact_line = " | ".join(contact_parts)
            self.cell(0, 6, contact_line, ln=True, align="C")

        self.ln(6)

    def add_section_title(self, title: str):
        """Add a section title with line extending from text to right margin."""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(70, 130, 180)  # Steel blue

        # Get the width of the title text
        title_text = title.upper()
        title_width = self.get_string_width(title_text) + 4

        # Draw title
        self.cell(title_width, 7, title_text, ln=False)

        # Draw line from title end to right margin
        y_pos = self.get_y() + 3.5
        self.set_draw_color(70, 130, 180)
        self.line(self.get_x() + 2, y_pos, 192, y_pos)

        self.set_text_color(0, 0, 0)  # Reset to black
        self.ln(10)

    def add_summary(self, summary: str):
        """Add professional summary/profile section."""
        if not summary:
            return

        self.add_section_title("Profile")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, summary, align="J")
        self.ln(4)

    def add_skills(self, skills):
        """Add technical skills section as flat comma-separated list."""
        if not skills:
            return

        self.add_section_title("Technical Skills")
        self.set_font("Helvetica", "", 10)

        # Handle both dict (categorized) and list (flat) formats
        if isinstance(skills, dict):
            all_skills = []
            for category, skill_list in skills.items():
                if isinstance(skill_list, list):
                    all_skills.extend(skill_list)
                elif skill_list:
                    all_skills.append(str(skill_list))
            skills_text = ", ".join(all_skills)
        elif isinstance(skills, list):
            skills_text = ", ".join(skills)
        else:
            skills_text = str(skills)

        self.multi_cell(0, 5, skills_text, align="J")
        self.ln(4)

    def add_education(self, education: list):
        """Add education section with bullet format."""
        if not education:
            return

        self.add_section_title("Education")

        for edu in education:
            # Build the education line: • Degree - Institution | Location | Dates
            degree = edu.get("degree", "")
            if edu.get("field"):
                degree += f" in {edu['field']}"

            parts = []
            if edu.get("institution"):
                parts.append(edu["institution"])
            if edu.get("location"):
                parts.append(edu["location"])
            if edu.get("dates"):
                parts.append(edu["dates"])

            # Bullet and bold degree
            self.set_font("Helvetica", "B", 10)
            bullet_degree = f"- {degree}"
            degree_width = self.get_string_width(bullet_degree) + 2
            self.cell(degree_width, 6, bullet_degree, ln=False)

            # Rest of the line in normal weight
            if parts:
                self.set_font("Helvetica", "", 10)
                rest = " - " + " | ".join(parts)
                self.cell(0, 6, rest, ln=True)
            else:
                self.ln(6)

        self.ln(4)

    def add_experience(self, experiences: list):
        """Add work experience section."""
        if not experiences:
            return

        self.add_section_title("Experience")

        for exp in experiences:
            # Line 1: Job title (bold)
            self.set_font("Helvetica", "B", 10)
            self.cell(0, 6, exp.get("title", ""), ln=True)

            # Line 2: Company | Type | Location with dates right-aligned
            company_parts = []
            if exp.get("company"):
                company_parts.append(exp["company"])
            if exp.get("type"):
                company_parts.append(exp["type"])
            if exp.get("location"):
                company_parts.append(exp["location"])

            company_line = " | ".join(company_parts)
            dates = exp.get("dates", "")

            self.set_font("Helvetica", "B", 10)
            self.cell(0, 5, company_line, ln=False)
            self.set_font("Helvetica", "", 10)
            self.cell(0, 5, dates, ln=True, align="R")

            self.ln(2)

            # Bullet points
            for bullet in exp.get("bullets", []):
                self._add_bullet_point(bullet)

            self.ln(4)

    def add_projects(self, projects: list):
        """Add projects section."""
        if not projects:
            return

        self.add_section_title("Projects")

        for project in projects:
            # Project name (bold)
            self.set_font("Helvetica", "B", 10)
            self.cell(0, 6, project.get("name", ""), ln=True)

            # Technologies if present
            if project.get("technologies"):
                self.set_font("Helvetica", "", 9)
                techs = project["technologies"]
                if isinstance(techs, list):
                    techs = ", ".join(techs)
                self.cell(0, 5, techs, ln=True)

            # Description if present
            if project.get("description"):
                self.set_font("Helvetica", "", 10)
                self.multi_cell(0, 5, project["description"], align="J")

            # Bullet points
            for bullet in project.get("bullets", []):
                self._add_bullet_point(bullet)

            self.ln(3)

    def add_certifications(self, certifications: list):
        """Add certifications section."""
        if not certifications:
            return

        self.add_section_title("Certifications")
        self.set_font("Helvetica", "", 10)

        for cert in certifications:
            # Format: • Certification Name - Issuer | Date
            cert_parts = []
            cert_name = cert.get("name", "")
            if cert.get("issuer"):
                cert_parts.append(cert["issuer"])
            if cert.get("date"):
                cert_parts.append(cert["date"])

            cert_line = f"- {cert_name}"
            if cert_parts:
                cert_line += " - " + " | ".join(cert_parts)

            self.cell(0, 6, cert_line, ln=True)

        self.ln(4)

    def add_references(self, references=None):
        """Add references section."""
        self.add_section_title("References")
        self.set_font("Helvetica", "", 10)

        if references and isinstance(references, list) and len(references) > 0:
            # List actual references if provided
            for ref in references:
                name = ref.get("name", "")
                title = ref.get("title", "")
                company = ref.get("company", "")
                contact = ref.get("contact", "")

                ref_line = f"- {name}"
                if title:
                    ref_line += f", {title}"
                if company:
                    ref_line += f" at {company}"
                if contact:
                    ref_line += f" - {contact}"

                self.cell(0, 6, ref_line, ln=True)
        else:
            # Default: Available upon request
            self.cell(0, 6, "Available upon request", ln=True)

        self.ln(4)


def generate_pdf(resume_data: dict) -> bytes:
    """
    Generate a PDF from structured resume data.

    Args:
        resume_data: Dictionary containing resume sections.

    Returns:
        PDF as bytes.
    """
    pdf = ResumePDF()

    # Use professional_title if available, otherwise fall back to first job title
    title = resume_data.get("professional_title", "")
    if not title:
        experiences = resume_data.get("experience", [])
        if experiences and experiences[0].get("title"):
            title = experiences[0]["title"]

    # Header with name and contact
    pdf.add_header(
        resume_data.get("name", ""),
        resume_data.get("contact", {}),
        title=title,
    )

    # Profile/Summary
    pdf.add_summary(resume_data.get("summary", ""))

    # Technical Skills
    pdf.add_skills(resume_data.get("skills", {}))

    # Education
    pdf.add_education(resume_data.get("education", []))

    # Experience
    pdf.add_experience(resume_data.get("experience", []))

    # Projects (if any)
    pdf.add_projects(resume_data.get("projects", []))

    # Certifications (if any)
    pdf.add_certifications(resume_data.get("certifications", []))

    # References
    pdf.add_references(resume_data.get("references", None))

    # Output to bytes
    return bytes(pdf.output())
