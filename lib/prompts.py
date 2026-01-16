"""LLM prompt templates for resume processing."""

STRUCTURE_RESUME_PROMPT = """You are a resume parser. Extract and structure the following resume text into a clean JSON format.

Resume Text:
{resume_text}

Return a JSON object with these sections (only include sections that exist in the resume):
- name: Full name
- contact: Object with email, phone, location, linkedin, github, website (as available)
- summary: Professional summary or objective (if present)
- experience: Array of objects with company, title, dates, location, type (e.g., "Remote"), bullets (array of achievements)
- education: Array of objects with institution, degree, field, location, dates, gpa (if mentioned)
- skills: Array of skill strings as a flat list (e.g., ["Python", "JavaScript", "AWS", "Docker"])
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
   - Reordering skills to prioritize job-relevant ones first (skills should be a flat array of strings)
   - Adjusting bullet points to emphasize relevant experience (without fabricating)
   - Incorporating relevant keywords naturally where appropriate
   - Strengthening action verbs and quantifiable achievements
3. Preserve:
   - All factual information (dates, companies, titles, education, certifications)
   - The overall structure and format
   - Professional tone
4. Skills must be a flat array of strings, not categorized (e.g., ["Python", "AWS", "Docker"])
5. Include certifications if present in the original resume

Return the optimized resume as a JSON object with the same structure as the input.
Return ONLY valid JSON, no markdown formatting or explanation."""
