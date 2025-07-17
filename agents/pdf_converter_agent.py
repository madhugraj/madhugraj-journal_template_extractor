# agents/pdf_converter_agent.py

import os
import subprocess
from langgraph.state_schema import AgentState

PDF_DIR = "media/pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

def convert_to_pdf(state: AgentState) -> AgentState:
    input_path = state.file_path
    filename = os.path.basename(input_path)
    filename_wo_ext, ext = os.path.splitext(filename)
    output_pdf = os.path.join(PDF_DIR, f"{filename_wo_ext}.pdf")

    if input_path.endswith(".pdf"):
        print("✅ Already a PDF. Skipping conversion.")
        state.pdf_path = input_path
        return state

    if os.path.exists(output_pdf):
        print(f"⚠️ PDF already exists: {output_pdf} — Skipping reconversion.")
        state.pdf_path = output_pdf
        return state

    try:
        print(f"🔄 Converting {input_path} to PDF...")
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", input_path, "--outdir", PDF_DIR
        ], check=True)
        print(f"📄 Converted to PDF: {output_pdf}")
        state.pdf_path = output_pdf
    except Exception as e:
        print(f"❌ PDF conversion failed: {e}")
        raise

    return state
