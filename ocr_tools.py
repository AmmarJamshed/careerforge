# ocr_tools.py
import streamlit as st
import tempfile
import os

# Try imports that may not be available in all environments
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except Exception:
    PDF2IMAGE_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except Exception:
    TESSERACT_AVAILABLE = False

# Fallback for text-based PDFs
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except Exception:
    PYPDF_AVAILABLE = False

def extract_text_with_pypdf(path_or_bytes):
    """Extract text from digital (searchable) PDF using pypdf (fast, no native deps)."""
    try:
        if isinstance(path_or_bytes, (bytes, bytearray)):
            # write to temp and read
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(path_or_bytes)
                tmp_path = tmp.name
            reader = PdfReader(tmp_path)
            os.remove(tmp_path)
        else:
            reader = PdfReader(path_or_bytes)
        text = []
        for p in reader.pages:
            txt = p.extract_text()
            if txt:
                text.append(txt)
        return "\n".join(text)
    except Exception as e:
        return ""

def extract_images_from_pdf(path_or_bytes, poppler_path=None):
    """Use pdf2image.convert_from_path when available. Accepts path or bytes."""
    if not PDF2IMAGE_AVAILABLE:
        raise RuntimeError("pdf2image not available")
    # if bytes, write temp file
    if isinstance(path_or_bytes, (bytes, bytearray)):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(path_or_bytes)
            tmp_path = tmp.name
    else:
        tmp_path = path_or_bytes

    try:
        if poppler_path:
            pages = convert_from_path(tmp_path, dpi=300, poppler_path=poppler_path)
        else:
            pages = convert_from_path(tmp_path, dpi=300)
        return pages
    finally:
        if isinstance(path_or_bytes, (bytes, bytearray)):
            try:
                os.remove(tmp_path)
            except:
                pass

def images_to_text(images):
    """Run pytesseract on PIL images and concatenate text."""
    if not TESSERACT_AVAILABLE:
        raise RuntimeError("pytesseract not available")
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# ---- Streamlit UI + orchestrator ----
def eligibility_engine():
    st.title("📄 OCR-Based Eligibility Engine (Robust)")

    st.markdown("""
    This engine will:
    - Prefer `pdf2image + pytesseract` for scanned PDFs (images).  
    - Fall back to `pypdf` text extraction for digital (searchable) PDFs if pdf2image/Poppler isn't available.
    """)

    st.info("If you have Poppler installed and Tesseract available, the engine will use OCR for scanned PDFs.")

    uploaded = st.file_uploader("Upload Transcript PDF (or test with the built-in sample)", type=["pdf"])

    # quick test button for your uploaded document on this machine
    if st.button("Run OCR on sample uploaded PDF path (local)"):
        # developer note: use the path you uploaded earlier - local path:
        sample_path = "/mnt/data/Careerforge Business Document.pdf"
        if os.path.exists(sample_path):
            st.write(f"Using local path: `{sample_path}`")
            _process_pdf_file(sample_path)
        else:
            st.error(f"Sample file not found at {sample_path}")

    if uploaded:
        # uploaded is a BytesIO-like object
        _process_pdf_file(uploaded)

def _process_pdf_file(uploaded_file):
    """
    uploaded_file: can be UploadedFile (has .read()) or a filesystem path string.
    """
    # detect whether we got a path (string) or uploaded bytes
    if isinstance(uploaded_file, str):
        path_or_bytes = uploaded_file
    else:
        # Streamlit uploaded file: read bytes
        path_or_bytes = uploaded_file.read()

    # 1) If pdf2image + pytesseract available, attempt image OCR (best for scanned)
    if PDF2IMAGE_AVAILABLE and TESSERACT_AVAILABLE:
        st.info("Attempting image-based OCR (pdf2image + pytesseract)...")
        try:
            # If your deployment needs a poppler path (Windows), set poppler_path variable.
            poppler_path = None  # e.g., r"C:\\path\\to\\poppler-23.01.0\\Library\\bin"
            pages = extract_images_from_pdf(path_or_bytes, poppler_path=poppler_path)
            text = images_to_text(pages)
            if text.strip():
                st.success("OCR (image) succeeded. Extracted text (preview):")
                st.write(text[:2000])
                _eligibility_decision_from_text(text)
                return
            else:
                st.warning("Image OCR produced empty text; trying text-extraction fallback...")
        except Exception as e:
            st.warning(f"Image OCR failed: {e}. Trying text-extraction fallback...")

    # 2) Fallback: try textual extraction with pypdf
    if PYPDF_AVAILABLE:
        st.info("Attempting text extraction (pypdf) for digital PDF...")
        try:
            if isinstance(path_or_bytes, (bytes, bytearray)):
                # write to temp file for pypdf
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(path_or_bytes)
                    tmp_path = tmp.name
                text = extract_text_with_pypdf(tmp_path)
                try:
                    os.remove(tmp_path)
                except:
                    pass
            else:
                text = extract_text_with_pypdf(path_or_bytes)

            if text.strip():
                st.success("Text extraction succeeded. Extracted text (preview):")
                st.write(text[:2000])
                _eligibility_decision_from_text(text)
                return
            else:
                st.warning("Text extraction returned empty string.")
        except Exception as e:
            st.error(f"Text extraction failed: {e}")

    # 3) If we reach here -> show error instructions
    st.error("Could not extract text. Install Poppler (for pdf2image) and Tesseract (for pytesseract) "
             "or ensure the PDF is not a scanned image-only file.")

def _eligibility_decision_from_text(text):
    """
    Dummy eligibility logic: detects numbers that look like percents for 'Matric' and 'Inter'
    and gives a simple recommendation. You should replace with your real logic.
    """
    import re
    # find percentages like 85% or 85.5%
    nums = re.findall(r"(\\d{2,3}(?:\\.\\d+)?)[\\s]*%?", text)
    nums = [float(n) for n in nums if float(n) <= 100]
    st.subheader("Dummy Eligibility Result")
    if len(nums) >= 2:
        matric = nums[0]
        inter = nums[1]
        st.write(f"Detected grades — Matric: {matric}%, Inter: {inter}% (first two numbers found)")
        if inter >= 85:
            st.success("Eligible for top-tier Pakistani universities (NUST, GIKI, FAST).")
        elif inter >= 70:
            st.success("Eligible for mid-tier universities.")
        else:
            st.info("Consider upskilling and improving grades for competitive universities.")
    else:
        st.info("Couldn't detect clear grade percentages — please enter grades manually in the Eligibility form.")
