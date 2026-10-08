# AI-Powered Invoice Processor

A small Python invoice-processing example that extracts text from a PDF, uses the Google Gemini API to structure the invoice data, validates the response with Pydantic, and writes the result to JSON. An n8n workflow export is included as a starting point for automation.

## Processing flow

1. Read `invoice.pdf` from the current working directory.
2. Extract text from each PDF page with `pypdf`.
3. Send the extracted text to Gemini and request structured output.
4. Validate the result against the invoice schema.
5. Write the extracted fields to `invoice_output.json`.

The output contains `vendor_name`, `invoice_number`, `invoice_date` (expected as `YYYY-MM-DD`), `total_amount`, and `tax_amount`.

## Requirements

- Python 3.9 or newer
- A Google Gemini API key

Install the Python dependencies:

```powershell
py -m pip install google-genai pypdf pydantic python-dotenv
```

Create a `.env` file in the project directory and add your API key:

```dotenv
GEMINI_API_KEY=your_api_key_here
```

Keep `.env` private and do not commit API keys or sensitive invoice documents.

## Run

Place the input document at `invoice.pdf` in the project directory, then run from that directory:

```powershell
py processor.py
```

On success, the extracted data is printed and written to `invoice_output.json`. The input filename is currently fixed in `processor.py`; the script does not yet accept a command-line path. PDF text extraction also depends on the PDF containing a readable text layer.

## n8n workflow

`n8nworkflow.json` describes a webhook-to-command-to-file-read flow. It is currently a draft rather than an import-ready workflow: the node `position` fields are incomplete, and the execute/read-file nodes contain machine-specific absolute Windows paths. Complete those fields and update the paths for the machine running n8n before importing or executing it. The Execute Command node must run in an environment with the Python dependencies and Gemini API key configured.

## Project files

- `processor.py` - PDF text extraction and Gemini structured-data extraction.
- `n8nworkflow.json` - Draft n8n automation workflow.
- `invoice.pdf` - Expected input filename; provide your own document.
- `invoice_output.json` - Generated JSON output (also currently contains an example result).