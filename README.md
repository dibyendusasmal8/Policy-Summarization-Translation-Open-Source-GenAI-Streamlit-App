# Policy Summarization & Translation — Open-Source GenAI Streamlit App

## What this is
A runnable Streamlit web app that:
- Accepts PDF/DOCX/TXT/Images or pasted text
- Summarizes policies/documents using Hugging Face transformers
- Translates summary between English and Bengali
- Stores records in a local SQLite database

## Quick start (local)
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *If you want CPU-only small install, consider replacing `facebook/bart-large-cnn` with `sshleifer/distilbart-cnn-12-6` and install a CPU-only torch wheel.*
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Open http://localhost:8501

## File structure
- app.py
- models.py
- utils.py
- db.py
- requirements.txt
- Dockerfile
- README.md

## Notes
- For production serving or many users, serve models separately (FastAPI/Gunicorn) and call via HTTP.
- For GPU usage set device=0 in pipeline() calls and install CUDA-enabled torch.

