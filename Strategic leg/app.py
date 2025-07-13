from flask import Flask, render_template, request, send_file
from utils import extract_text_from_pdf, summarize_legal_document, export_summary_to_pdf
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            full_text, page_refs = extract_text_from_pdf(file_path)
            summary_items = summarize_legal_document(full_text)

            # ✅ Generate PDF here
            pdf_path = "summary_output.pdf"
            export_summary_to_pdf(summary_items, pdf_path)

            return render_template("index.html", summaries=summary_items, refs=page_refs)
    return render_template("index.html", summaries=None)


@app.route("/download")
def download_pdf():
    return send_file("summary_output.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
