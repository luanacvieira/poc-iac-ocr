# extract_info.py
# Script para extração de informações
import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_fields_from_text(text, prompt):
    name_match = re.search(r"(?:Nome[:\s]*)?([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
    date_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    value_match = re.search(r"R\$ ?[\d.,]+", text)

    name = name_match.group(1) if name_match else "Não encontrado"
    date = date_match.group(1) if date_match else "Não encontrado"
    value = value_match.group(0) if value_match else "Não encontrado"

    return f"Nome: {name}, Data: {date}, Valor: {value}"
