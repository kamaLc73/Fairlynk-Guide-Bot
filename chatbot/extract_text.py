import pdfplumber
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def extract_text_from_pdf(pdf_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    logging.info(f"Texte extrait et sauvegardé dans {output_path}")

if __name__ == "__main__":
    pdf_path = "data/guide_fairlynk.pdf"
    output_path = "data/guide_fairlynk.txt"
    extract_text_from_pdf(pdf_path, output_path)