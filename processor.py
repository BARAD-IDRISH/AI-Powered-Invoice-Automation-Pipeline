import os
import json
from pypdf import PdfReader
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

load_dotenv()


client = genai.Client()

# 2. Define the exact JSON schema using Pydantic for rigid validation mapping
class InvoiceSchema(BaseModel):
    vendor_name: str = Field(description="The name of the company or vendor issuing the invoice.")
    invoice_number: str = Field(description="The unique invoice identifier or invoice number.")
    invoice_date: str = Field(description="The billing date converted to YYYY-MM-DD format.")
    total_amount: float = Field(description="The final total balance due on the invoice as a plain number.")
    tax_amount: float = Field(description="The tax or VAT value charged on the invoice as a plain number.")

def parse_invoice_pdf(file_path):
    """Reads raw text layers from an invoice PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"File Error: Failed to read PDF at {file_path}. {e}")
        return None

def extract_invoice_with_gemini(invoice_text):
    """Queries Gemini to map text directly into the strict Pydantic JSON blueprint."""
    prompt = f"""
    You are an automated accounting extraction agent. 
    Analyze the following raw text from a business invoice document and pull all required fields.
    
    Invoice Raw Text:
    \"\"\"{invoice_text}\"\"\"
    """
    try:
        # Utilizing gemini-2.0-flash for high-speed document extraction
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': InvoiceSchema, # Forces Gemini to strictly output the Pydantic schema
            },
        )
        # Parse returned string back into a clean visual JSON format
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"Gemini API Error: Data extraction failed. {e}")
        return None

if __name__ == "__main__":

    import sys; sys.stdout.reconfigure(encoding='utf-8') 
   
    target_invoice = "invoice.pdf"
    
    print("🔄 Step 1: Parsing text from PDF document...")
    raw_text = parse_invoice_pdf(target_invoice)
    
    if raw_text:
        print("🤖 Step 2: Extracting data with Gemini API Structured Outputs...")
        extracted_data = extract_invoice_with_gemini(raw_text)
        
        if extracted_data:
            print("\n🎉 Extraction Successful! Gemini JSON Payload:")
            print(json.dumps(extracted_data, indent=4))
            
            # Export structured data locally for n8n payload pickup
            with open("invoice_output.json", "w") as out_file:
                json.dump(extracted_data, out_file)
