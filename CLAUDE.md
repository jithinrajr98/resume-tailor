# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Resume Tailor is a Streamlit web application that optimizes resumes for specific job descriptions using LLM-powered analysis. Users upload a PDF resume, paste a job description, and receive a tailored resume as a downloadable PDF.

## Commands

### Setup (using uv)
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Environment
Copy `.env.example` to `.env` and add your Groq API key:
```bash
cp .env.example .env
```

### Run the application
```bash
streamlit run app.py
```

## Architecture

The application follows a linear pipeline:

1. **PDF Upload** → `lib/pdf_parser.py` extracts text using pdfplumber
2. **Structure** → `lib/groq_client.py:structure_resume()` converts raw text to JSON via Groq/Llama 3.3 70B
3. **Optimize** → `lib/groq_client.py:optimize_resume()` tailors the structured resume to a job description
4. **Generate** → `lib/pdf_generator.py` renders the optimized JSON back to PDF using fpdf2

### Key Files
- `app.py` - Streamlit UI with session state managing the 4-step workflow
- `lib/prompts.py` - LLM prompt templates for parsing and optimization
- `lib/groq_client.py` - Groq API integration (model: llama-3.3-70b-versatile), supports both `st.secrets` (Streamlit Cloud) and environment variables
- `lib/pdf_generator.py` - `ResumePDF` class handles PDF layout and rendering

### Resume JSON Schema
The structured resume format includes: `name`, `professional_title`, `contact`, `summary`, `experience`, `education`, `skills`, `projects`, `certifications`. See `lib/prompts.py` for the full schema definition.

## Deployment

For Streamlit Community Cloud, add `GROQ_API_KEY` in the app's Secrets settings. The app automatically uses `st.secrets` when deployed.
