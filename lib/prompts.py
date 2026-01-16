"""LLM prompt templates for resume processing."""

STRUCTURE_RESUME_PROMPT = """You are a resume parser. Extract and structure the following resume text into a clean JSON format.

Resume Text:
{resume_text}

Return a JSON object with these sections (only include sections that exist in the resume):
- name: Full name
- contact: Object with email, phone, location, linkedin, github, website (as available)
- summary: Professional summary or objective (if present)
- experience: Array of objects with company, title, dates, location, bullets (array of achievements)
- education: Array of objects with institution, degree, field, dates, gpa (if mentioned)
- skills: Object with categories as keys and arrays of skills as values (e.g., "Programming Languages": ["Python", "JavaScript"])
- projects: Array of objects with name, description, technologies, bullets (if present)
- certifications: Array of objects with name, issuer, date (if present)

Return ONLY valid JSON, no markdown formatting or explanation."""

OPTIMIZE_RESUME_PROMPT = """You are an expert resume optimizer. Your task is to fine-tune a resume for a specific job description while preserving the original style, structure, and truthfulness.

Original Resume (JSON):
{resume_json}

Job Description:
{job_description}

Instructions:
1. Identify key skills, technologies, and requirements from the job description
2. Enhance the resume by:
   - Reordering skills to prioritize relevant ones
   - Adjusting bullet points to emphasize relevant experience (without fabricating)
   - Incorporating relevant keywords naturally where appropriate
   - Strengthening action verbs and quantifiable achievements
3. Preserve:
   - All factual information (dates, companies, titles, education)
   - The overall structure and format
   - Professional tone

Return the optimized resume as a JSON object with the same structure as the input.
Return ONLY valid JSON, no markdown formatting or explanation."""
