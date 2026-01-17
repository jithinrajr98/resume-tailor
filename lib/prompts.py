"""LLM prompt templates for resume processing."""

STRUCTURE_RESUME_PROMPT = """You are a resume parser. Extract and structure the following resume text into a clean JSON format.

Resume Text:
{resume_text}

Return a JSON object with these sections (only include sections that exist in the resume):
- name: Full name
- professional_title: Professional title/role (e.g., "Machine Learning Engineer", "Software Developer")
- contact: Object with email, phone, location, linkedin, github, website (as available)
- summary: Professional summary or objective (if present)
- experience: Array of objects with company, title, dates, location, type (e.g., "Remote"), bullets (array of achievements)
- education: Array of objects with institution, degree, field, location, dates, gpa (if mentioned)
- skills: Array of skill strings as a flat list (e.g., ["Python", "JavaScript", "AWS", "Docker"])
- projects: Array of objects with name, description, technologies, bullets (if present)
- certifications: Array of objects with name, issuer, date (if present)
- references: Array of objects with name, title, company, contact (if present in resume)

Return ONLY valid JSON, no markdown formatting or explanation."""

OPTIMIZE_RESUME_PROMPT = """You are an expert resume optimizer. Your task is to fine-tune a resume for a specific job description while preserving the original style, structure, and truthfulness.

Original Resume (JSON):
{resume_json}

Job Description:
{job_description}

Instructions:
1. Identify key skills, technologies, and requirements from the job description
2. Enhance the resume by:
   - Updating professional_title to match the target job role (e.g., if applying for "Machine Learning Engineer", use that as the professional_title)
   - Reordering skills to prioritize job-relevant ones first (skills should be a flat array of strings)
   - Adjusting bullet points to emphasize relevant experience (without fabricating)
   - Incorporating relevant keywords naturally where appropriate
   - Strengthening action verbs and quantifiable achievements
   - Using diverse vocabulary - avoid repeating words like "demonstrating", "showcasing", "leveraging", "utilizing"; each bullet should use distinct action verbs
   - Do not use the word "Spearheaded"
3. Preserve:
   - All factual information (dates, companies, job titles, education, certifications)
   - The overall structure and format
   - Professional tone
   - References section exactly as provided (do not modify contact information)
4. Skills must be a flat array of strings, not categorized (e.g., ["Python", "AWS", "Docker"])
5. Include certifications if present in the original resume
6. Language quality: Vary action verbs across bullet points. Avoid filler words and repetitive phrasing. Each achievement should read distinctly.

Return the optimized resume as a JSON object with the same structure as the input.
Return ONLY valid JSON, no markdown formatting or explanation."""
