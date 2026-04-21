DDR AI Report Generator

This project is an end-to-end AI pipeline that converts raw inspection and thermal reports into a structured, client-ready Detailed Diagnostic Report (DDR).

The goal of this system is not just to generate text, but to handle real-world challenges like incomplete data, conflicting observations, and unstructured inputs, while maintaining clarity and reliability.

---

What this system does

Given two input documents:

* Inspection Report (PDF)
* Thermal Report (PDF)

The system automatically:

* Extracts text from both documents
* Cleans and preprocesses the data
* Identifies key observations
* Extracts relevant images from PDFs
* Combines inspection and thermal insights
* Handles missing and conflicting information
* Generates a structured DDR report
* Saves the final output as a formatted PDF with images

---

Project Structure

data/
report.pdf
thermal.pdf

src/
extract_text.py
extract_images.py
preprocess.py
ai.py
report_generator.py
pipeline.py

output/
images/
final_ddr.pdf

app.py
api.py
README.md

---

How to run the project

1. Clone the repository

git clone <your-repo-link>
cd DDR-AI-Project

2. Create virtual environment

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Set API key (required)

For Windows (PowerShell):

$env:GROQ_API_KEY="your_api_key_here"

5. Run the pipeline (CLI)

python app.py

6. Run as API (recommended)

uvicorn api:app

Open in browser:
http://127.0.0.1:8000/docs

Click /generate → Execute

---

Output

The system generates:

output/final_ddr.pdf

The report includes:

* Property Issue Summary
* Area-wise Observations
* Probable Root Cause
* Severity Assessment
* Recommended Actions
* Additional Notes
* Missing or Unclear Information

Images extracted from the reports are placed within relevant sections to support findings.

---

Key Design Decisions

* Modular pipeline architecture for clarity and maintainability
* Separation of extraction, preprocessing, AI reasoning, and report generation
* Prompt-controlled AI output to avoid hallucination
* Fallback system to ensure output even if AI fails
* API layer added to simulate production usage

---

Handling Real-World Challenges

Missing Information:
If any required data is not available, the system explicitly outputs "Not Available".

Conflicting Data:
If inspection and thermal reports contradict each other, the system highlights it as "Conflict Detected".

Unstructured Input:
The preprocessing layer cleans and structures raw text before passing it to the model.

---

Limitations

* Image placement is currently sequential and not semantically mapped
* Duplicate detection is handled through prompting rather than strict logic
* Model output depends on token limits and prompt quality

---

Future Improvements

* Semantic mapping between images and observations
* Better conflict detection using structured reasoning
* Evaluation metrics for report quality
* Async processing for large-scale usage
* Deployment using Docker or cloud services

---

Why this project matters

This project focuses on building a practical AI workflow rather than just using a model. It demonstrates how to design a system that is reliable, structured, and usable in real-world scenarios.

---

Author

Harsh Thanki
