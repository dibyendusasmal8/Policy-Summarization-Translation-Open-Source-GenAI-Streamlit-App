import streamlit as st
from models import get_summarizer, get_translator_en_bn, get_translator_bn_en, summarize_text, translate_text
from utils import extract_text_from_pdf, extract_text_from_docx, ocr_image
from db import init_db, SessionLocal, create_document
import io

init_db()

st.set_page_config(page_title="Policy Summarizer & Translator", layout='centered')
st.title("Policy Summarizer & Translator — Open Source LLMs")

with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Summarizer model", ["facebook/bart-large-cnn", "sshleifer/distilbart-cnn-12-6"])
    device_choice = st.selectbox("Device", ["cpu", "gpu"])
    summary_length = st.radio("Summary length", ["short", "medium", "long"])

length_map = {"short": (40, 80), "medium": (80, 180), "long": (180, 400)}
min_len, max_len = length_map[summary_length]

uploaded = st.file_uploader("Upload policy file (PDF/DOCX/TXT/PNG/JPG)", type=["pdf","docx","txt","png","jpg","jpeg"])
raw_text = st.text_area("Or paste text here", height=200)

if uploaded is not None:
    file_bytes = uploaded.read()
    file_stream = io.BytesIO(file_bytes)
    # guess by suffix/type
    name = getattr(uploaded, 'name', '')
    if name.lower().endswith('.pdf') or uploaded.type == "application/pdf":
        text = extract_text_from_pdf(file_stream)
    elif name.lower().endswith('.docx') or uploaded.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        file_stream.seek(0)
        text = extract_text_from_docx(file_stream)
    elif uploaded.type.startswith("image"):
        file_stream.seek(0)
        text = ocr_image(file_stream)
    else:
        try:
            text = file_bytes.decode('utf-8', errors='ignore')
        except:
            text = ""
else:
    text = raw_text

if st.button("Generate summary"):
    if not text or text.strip() == "":
        st.error("Please provide text or upload a file.")
    else:
        st.info("Loading model and generating summary (this may take time on first run)...")
        device = -1
        if device_choice == "gpu":
            device = 0
        summarizer = get_summarizer(model_choice, device)
        summary = summarize_text(text, summarizer, max_length=max_len, min_length=min_len)
        st.subheader("Summary")
        st.write(summary)

        st.subheader("Translation")
        translation_text = None
        if st.button("Translate summary to Bengali"):
            st.info("Translating to Bengali...")
            translator = get_translator_en_bn()
            bn = translate_text(summary, translator)
            st.write(bn)
            translation_text = bn
        if st.button("Translate summary to English"):
            st.info("Translating to English...")
            translator = get_translator_bn_en()
            en = translate_text(summary, translator)
            st.write(en)
            translation_text = en

        # save to DB
        db = SessionLocal()
        doc = create_document(db, filename=getattr(uploaded, 'name', None), original_text=text, summary=summary, translation=translation_text)
        st.success(f"Saved to DB with id {doc.id}")
