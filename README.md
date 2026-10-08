# AI-Powered Business Document & Invoice Automation Pipeline

An end-to-end local document intelligence system that extracts unstructured accounting layers from business invoice PDFs into structured JSON data structures, orchestrated through a self-hosted automation runtime.

### 🛠️ Tech Stack & Requirements
- **Python Version:** Python 3.9 or newer
- **AI Core Engine:** Google Gemini API (**`gemini-3.8-flash`**) via the modern `google-genai` SDK
- **Data Validation:** Pydantic (Structured Output Schema mapping)
- **Orchestration Hub:** n8n Workflow Automation Server (Self-hosted SQLite runtime instance)
- **Database Tracking:** Local JSON Payloads & Google Sheets Cloud Integration

### 📋 Installation & Environment Setup
Install the project dependencies natively via your package manager:
```bash
pip install google-genai pydantic pypdf python-dotenv
```

Create a text file named exactly `.env` in the root project directory and securely save your Google AI Studio credential string (do not use quotes or spaces):
```env
GEMINI_API_KEY=AIzaSyYourActualSecretKeyHere
```
*Security Reminder: Keep `.env` private and ensure it is included in your `.gitignore` to prevent leaking active credentials to public repositories.*

### 🚀 Processing Flow & Execution
1. **Read & Extract:** The script targets a sample file at `invoice.pdf` in the working directory and extracts text layers across all pages via `pypdf`.
2. **Deterministic Processing:** The raw text payload is transmitted to the `gemini-3.8-flash` endpoint under strict `response_schema` constraints.
3. **Structured Ingestion:** Data is validated against the Pydantic template schema, converting the response into a structured output containing `vendor_name`, `invoice_number`, `invoice_date` (normalized to YYYY-MM-DD), `total_amount`, and `tax_amount`.
4. **Data Sync:** Outputs parameters cleanly to `invoice_output.json`.

Execute the script from your terminal using:
```bash
python processor.py
```

### 🔄 n8n Workflow Automation Mesh
The repository includes `n8nworkflow.json`, which maps out a robust Webhook-to-Command-to-File-Read execution pipeline. 

* **Infrastructure Configuration Note:** The included workflow blueprint serves as a structural guide. Before importing it into your active local n8n canvas (`http://localhost:5678`), ensure you configure the environment variables (`NODE_FUNCTION_ALLOW_BUILTIN="*"`) and update the terminal command execution strings to match your host machine's absolute Windows file directory paths.
