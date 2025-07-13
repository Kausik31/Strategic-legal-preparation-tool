import pdfplumber
import spacy
from transformers import pipeline
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(pdf_path):
    full_text = ""
    page_refs = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n\n--- Page {i+1} ---\n" + text
                page_refs.append(f"Page {i+1}: {text[:60]}...")
    return full_text, page_refs

def summarize_legal_document(text):
    chunks = []
    while len(text) > 1000:
        split_point = text[:1000].rfind('.')
        chunks.append(text[:split_point+1])
        text = text[split_point+1:]
    if text:
        chunks.append(text)

    summarized_points = []
    for chunk in chunks[:5]:  # limit for performance
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summarized_points.append(summary[0]['summary_text'])
    return summarized_points
def export_summary_to_pdf(summary_items, output_path="summary_output.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Top 10 Key Points from Legal Document")
    y -= 40

    c.setFont("Helvetica", 12)
    for idx, item in enumerate(summary_items, 1):
        text = f"{idx}. {item}"
        wrapped_lines = split_text(text, max_width=100)
        for line in wrapped_lines:
            if y < 80:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 12)
            c.drawString(50, y, line.strip())
            y -= 20
        y -= 10

    c.save()
    return output_path


def split_text(text, max_width=100):
    """Wrap long lines to fit inside the PDF width."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) <= max_width:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines
