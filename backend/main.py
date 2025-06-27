# main.py
# Ponto de entrada do backendfrom fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.extract_info import extract_fields_from_text
from backend.history_manager import add_to_history, load_history
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes
import os
import datetime
from fastapi import FastAPI
from fastapi import File, UploadFile, Form
from dotenv import load_dotenv  
load_dotenv()
# main.py


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    if not text.strip():  # Se não encontrar texto, usar OCR
        images = convert_from_bytes(content)
        for image in images:
            text += pytesseract.image_to_string(image)
    # Salva histórico
    record = {
        "filename": file.filename,
        "timestamp": datetime.datetime.now().isoformat(),
        "text_preview": text[:200]  # salva só um trecho do texto
    }
    add_to_history(record)
    return {"text": text}

@app.post("/analyze/")
async def analyze_text(text: str = Form(...), prompt: str = Form(...)):
    result = extract_fields_from_text(text, prompt)
    return JSONResponse(content={"result": result})

@app.get("/history/")
def get_history():
    return JSONResponse(content=load_history())

