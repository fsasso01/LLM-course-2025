import os
import requests
from llmsherpa.readers import Document
from llama_index.llms.groq import Groq
import time


my_groq_key = ""
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = my_groq_key

llm = Groq(model="llama-3.3-70b-versatile")

api_url = "http://127.0.0.1:5010/api/parseDocument?renderFormat=all"
pdf_path = os.path.join(os.getcwd(), "2024q1-alphabet-earnings-release-pdf.pdf")

print(f"Analizzo il file: {pdf_path}...")
try:
    with open(pdf_path, 'rb') as f:
        response = requests.post(api_url, files={'file': f})
        response.raise_for_status()
        json_data = response.json()
        
        if 'return_dict' in json_data:
            blocks_data = json_data['return_dict']['result']['blocks']
        else:
            blocks_data = json_data.get('returnDict', {}).get('result', {}).get('blocks')
            
    doc = Document(blocks_data)
    print("PDF correctly processed.")

except Exception as e:
    print(f"Docker error: {e}")
    exit()


full_context = ""
for section in doc.sections():
    full_context += section.to_html(include_children=True, recurse=True) + "\n"
safe_context = full_context[:20000]
print(f"Context ready ({len(safe_context)} characters).")

questions = [
    "Based on the 'Segment Operating Results' or Revenue tables, sum the 2024 revenues of 'Google Services', "
    "'Google Cloud', and 'Other Bets'. Does the sum match the 'Total revenues' listed? Show the math.",
    "Calculate the difference in dollars between the Operating Income of 2024 and 2023. Show the calculation."
]

print("\n--- REASONING TEST START ---")

for q in questions:
    time.sleep(5) 
    print(f"Question: {q}")
    
    resp = llm.complete(
        f"Context: {safe_context}\n\n"
        f"Task: Answer the question based ONLY on the provided context. "
        f"Step-by-step reasoning is required for calculations.\n"
        f"Question: {q}"
    )
    print(f"Response:\n{resp.text}")
    print("-" * 50)