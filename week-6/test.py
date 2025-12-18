import os
import requests
import json

# 1. SETUP
api_url = "http://127.0.0.1:5010/api/parseDocument?renderFormat=all"
pdf_path = os.path.join(os.getcwd(), "2024q1-alphabet-earnings-release-pdf.pdf")

print(f"Analizzo: {pdf_path}")

try:
    with open(pdf_path, 'rb') as f:
        # Invio a Docker
        response = requests.post(api_url, files={'file': f})
        
        # Se non è 200, stampa l'errore HTTP
        if response.status_code != 200:
            print(f"❌ Errore HTTP: {response.status_code}")
            print(response.text)
            exit()
            
        json_data = response.json()
        
        print("\n--- DEBUG STRUTTURA JSON ---")
        # Stampiamo le chiavi principali per capire cosa c'è dentro
        print(f"Chiavi trovate: {list(json_data.keys())}")
        
        if 'returnDict' not in json_data:
            print("\n⚠️ Manca 'returnDict'. Ecco un'anteprima del contenuto:")
            # Stampa i primi 500 caratteri del JSON formattato per capire l'errore
            print(json.dumps(json_data, indent=2)[:500])
        else:
            print("✅ 'returnDict' trovato! Il problema era altrove.")

except Exception as e:
    print(f"Errore: {e}")