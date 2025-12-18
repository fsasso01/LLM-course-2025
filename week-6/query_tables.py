import os
import requests
from llmsherpa.readers import Document
from llama_index.llms.groq import Groq


my_groq_key = ""
os.environ["GROQ_API_KEY"] = my_groq_key.strip()
print(f"Key set (length: {len(my_groq_key)} characters). Connection...")
try:
    llm = Groq(model="llama-3.3-70b-versatile", api_key=my_groq_key)
except Exception as e:
    print(f"Error config Groq: {e}")
    exit()

api_url = "http://127.0.0.1:5010/api/parseDocument?renderFormat=all"
pdf_path = os.path.join(os.getcwd(), "2024q1-alphabet-earnings-release-pdf.pdf")

try:
    with open(pdf_path, 'rb') as f:
        print("2. Docker: Analisi PDF...")
        response = requests.post(api_url, files={'file': f})
        response.raise_for_status()
        json_data = response.json()
        
        if 'return_dict' in json_data:
            blocks_data = json_data['return_dict']['result']['blocks']
        else:
            blocks_data = json_data.get('returnDict', {}).get('result', {}).get('blocks')

except Exception as e:
    print(f"Error Docker: {e}")
    exit()

doc = Document(blocks_data)
selected_section = None
for section in doc.sections():
    if 'Q1 2024 Financial Highlights' in section.title:
        selected_section = section
        break

if not selected_section:
    print("Section not found")
    exit()

context = selected_section.to_html(include_children=True, recurse=True)

questions = [
    "What was Google's operating margin for 2024?",
    "What % Net income is of the Revenues?"
]

print("\n--- GROQ RESPONSE ---")
for q in questions:
    print(f"\nQuestion: {q}")
    resp = llm.complete(f"Read the table inside the Context carefully. Answer the Question concisely using only the data provided.\nContext: {context}\nQuestion: {q}")
    print(f"Response: {resp.text}")