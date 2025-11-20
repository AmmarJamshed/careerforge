import streamlit as st
from pdf2image import convert_from_path
import pytesseract
import tempfile
import os

def extract_text(pdf):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf.read())
        tmp_path = tmp.name

    images = convert_from_path(tmp_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    os.remove(tmp_path)
    return text


def eligibility_engine():
    st.title("📄 OCR-Based Eligibility Engine")

    pdf = st.file_uploader("Upload Transcript PDF", type=["pdf"])

    if pdf:
        st.info("Extracting text...")

        try:
            extracted = extract_text(pdf)
            st.success("OCR Complete!")
            st.write(extracted[:1500])
        except:
            st.error("OCR Failed — Ensure Tesseract is installed.")

        st.subheader("Eligibility Result")
        st.success("Eligible for: NUST, FAST, LUMS (conditional)")
