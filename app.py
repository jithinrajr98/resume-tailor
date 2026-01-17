"""Resume Fine-Tuning Application - Streamlit UI."""

import streamlit as st
import json
from io import BytesIO

from lib.pdf_parser import extract_text_from_pdf
from lib.groq_client import structure_resume, optimize_resume, translate_resume
from lib.pdf_generator import generate_pdf

# Page configuration
st.set_page_config(
    page_title="Resume Tailor",
    page_icon="📄",
    layout="centered",
)

st.title("Resume Tailor")
st.markdown("Fine-tune your resume for specific job descriptions")

# Initialize session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "resume_structured" not in st.session_state:
    st.session_state.resume_structured = None
if "resume_optimized" not in st.session_state:
    st.session_state.resume_optimized = None
if "step" not in st.session_state:
    st.session_state.step = 1
if "resume_french" not in st.session_state:
    st.session_state.resume_french = None

# Step 1: Upload Resume
st.header("1. Upload Resume")
uploaded_file = st.file_uploader("Upload your PDF resume", type=["pdf"])

if uploaded_file is not None:
    if st.session_state.resume_text is None:
        with st.spinner("Extracting text from PDF..."):
            pdf_bytes = BytesIO(uploaded_file.read())
            st.session_state.resume_text = extract_text_from_pdf(pdf_bytes)

        with st.spinner("Structuring resume..."):
            try:
                st.session_state.resume_structured = structure_resume(
                    st.session_state.resume_text
                )
                st.session_state.step = 2
            except Exception as e:
                st.error(f"Error structuring resume: {str(e)}")

    if st.session_state.resume_structured:
        with st.expander("View extracted resume", expanded=False):
            st.json(st.session_state.resume_structured)

# Step 2: Paste Job Description
if st.session_state.step >= 2:
    st.header("2. Paste Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the full job description to optimize your resume for...",
    )

    if st.button("Optimize Resume", disabled=not job_description):
        with st.spinner("Optimizing resume for job description..."):
            try:
                st.session_state.resume_optimized = optimize_resume(
                    st.session_state.resume_structured, job_description
                )
                st.session_state.resume_french = None  # Reset French version
                st.session_state.step = 3
            except Exception as e:
                st.error(f"Error optimizing resume: {str(e)}")

# Step 3: Review Optimizations
if st.session_state.step >= 3 and st.session_state.resume_optimized:
    st.header("3. Review Optimized Resume")

    # Display optimized resume in editable JSON format
    optimized_json = st.text_area(
        "Edit the optimized resume (JSON format)",
        value=json.dumps(st.session_state.resume_optimized, indent=2),
        height=400,
    )

    # Parse and validate JSON on edit
    try:
        edited_resume = json.loads(optimized_json)
        st.session_state.resume_optimized = edited_resume
    except json.JSONDecodeError:
        st.warning("Invalid JSON format. Please fix the syntax.")
        edited_resume = None

    # Step 4: Download PDF
    if edited_resume:
        st.header("4. Download Resume")

        col1, col2 = st.columns(2)

        with col1:
            try:
                pdf_bytes = generate_pdf(st.session_state.resume_optimized)
                st.download_button(
                    label="Download PDF (English)",
                    data=pdf_bytes,
                    file_name="Jithin_Reghuvaran_CV.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

        with col2:
            if st.session_state.resume_french is None:
                if st.button("Generate French Version"):
                    with st.spinner("Translating resume to French..."):
                        try:
                            st.session_state.resume_french = translate_resume(
                                st.session_state.resume_optimized
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error translating resume: {str(e)}")
            else:
                try:
                    french_pdf_bytes = generate_pdf(st.session_state.resume_french)
                    st.download_button(
                        label="Download PDF (French)",
                        data=french_pdf_bytes,
                        file_name="Jithin_Reghuvaran_CV_FR.pdf",
                        mime="application/pdf",
                        key="french_pdf_download",
                    )
                except Exception as e:
                    st.error(f"Error generating French PDF: {str(e)}")

# Reset button
if st.session_state.step > 1:
    if st.button("Start Over"):
        st.session_state.resume_text = None
        st.session_state.resume_structured = None
        st.session_state.resume_optimized = None
        st.session_state.resume_french = None
        st.session_state.step = 1
        st.rerun()
