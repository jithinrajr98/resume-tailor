"""Groq API client for LLM operations."""

import json
import os
from groq import Groq
from dotenv import load_dotenv
from .prompts import STRUCTURE_RESUME_PROMPT, OPTIMIZE_RESUME_PROMPT, TRANSLATE_RESUME_PROMPT

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def get_client() -> Groq:
    """Get Groq client instance."""
    # Try st.secrets first (Streamlit Cloud), then fall back to env vars
    api_key = None
    try:
        import streamlit as st
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in secrets or environment variables")
    return Groq(api_key=api_key)


def structure_resume(resume_text: str) -> dict:
    """
    Use LLM to structure raw resume text into JSON format.

    Args:
        resume_text: Raw text extracted from PDF.

    Returns:
        Structured resume as a dictionary.
    """
    client = get_client()

    prompt = STRUCTURE_RESUME_PROMPT.format(resume_text=resume_text)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4000,
    )

    content = response.choices[0].message.content.strip()

    # Handle potential markdown code blocks
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    return json.loads(content)


def optimize_resume(resume_json: dict, job_description: str) -> dict:
    """
    Optimize resume for a specific job description.

    Args:
        resume_json: Structured resume as a dictionary.
        job_description: Target job description text.

    Returns:
        Optimized resume as a dictionary.
    """
    client = get_client()

    prompt = OPTIMIZE_RESUME_PROMPT.format(
        resume_json=json.dumps(resume_json, indent=2),
        job_description=job_description,
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000,
    )

    content = response.choices[0].message.content.strip()

    # Handle potential markdown code blocks
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    return json.loads(content)


def translate_resume(resume_json: dict, target_language: str = "French") -> dict:
    """
    Translate resume content to a target language.

    Args:
        resume_json: Structured resume as a dictionary.
        target_language: Target language for translation (default: French).

    Returns:
        Translated resume as a dictionary.
    """
    client = get_client()

    prompt = TRANSLATE_RESUME_PROMPT.format(
        resume_json=json.dumps(resume_json, indent=2),
        target_language=target_language,
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4000,
    )

    content = response.choices[0].message.content.strip()

    # Handle potential markdown code blocks
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    return json.loads(content)
