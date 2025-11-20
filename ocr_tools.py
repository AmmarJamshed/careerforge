import streamlit as st
from pypdf import PdfReader
import tempfile
from groq import Groq

# Load Groq API key
GROQ_KEY = st.secrets["GROQ_API_KEY"]

def extract_text_from_pdf(uploaded_file):
    """Extract text from ANY digital PDF using PyPDF."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    text = ""

    for page in reader.pages:
        try:
            text += page.extract_text() + "\n"
        except:
            pass

    return text


def analyze_with_groq(text):
    """Send extracted text to Groq for intelligent eligibility analysis."""
    client = Groq(api_key=GROQ_KEY)

    prompt = f"""
You are an AI admissions expert.

The following is a student's document text:

{text}

Please extract:

1. Student name (if present)
2. Degree / Program (if present)
3. All grades, percentages, or GPA mentioned
4. Whether this appears to be: transcript / certificate / SOP / resume / business document
5. Eligibility for Pakistani universities
6. Eligibility for International universities (UK, US, Germany, Turkey, Malaysia)
7. Recommendations for missing information

Return the result as clean readable text.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are an expert education counselor."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def eligibility_engine():
    st.title("📄 AI Document Analyzer (Groq-Powered)")

    uploaded = st.file_uploader("Upload Transcript / Certificate / SOP / Any PDF", type=["pdf"])

    if uploaded:
        st.info("Extracting text using PyPDF (no OCR)...")
        extracted_text = extract_text_from_pdf(uploaded)

        st.success("Text Extracted Successfully!")
        st.subheader("🔍 Extracted Text Preview")
        st.write(extracted_text[:2000])

        st.info("Sending extracted text to Groq for analysis...")
        groq_output = analyze_with_groq(extracted_text)

        st.success("AI Analysis Complete")
        st.subheader("📌 Eligibility & AI Insights")
        st.write(groq_output)
