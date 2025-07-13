# Strategic Legal Preparation Tool 

This AI-powered web app helps legal professionals analyze lengthy legal documents and extract the **top 10 most important points**, which are then exported as a downloadable PDF report.

## features
- Upload and process PDF legal documents
- NLP-based summarization using HuggingFace BART
- Highlights key arguments and generates a structured report
- Web interface using Flask
- Report export as PDF (via ReportLab)

##  Tech Stack
- Python 3
- Flask
- pdfplumber
- spaCy
- Transformers (BART model)
- ReportLab

How to run:

# 1. Clone the repository
git clone https://github.com/your-username/strategic-legal-preparation-tool.git
cd strategic-legal-preparation-tool

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install all required dependencies
pip install -r requirements.txt

# 4. Run the Flask app
python app.py

# 5. Open your browser and visit
http://127.0.0.1:5000

