import json
import os

MODELLO_DIR = "modello/"
OUTPUT_FILE = "modello/dataset_atomico_cyberwin.json"

def genera_dataset_atomico():
    print("\n--- GENERAZIONE DATASET ATOMICO TOTALE ---")
    training_data = []
    
    if not os.path.exists(MODELLO_DIR):
        print(f"[!] Errore: Cartella {MODELLO_DIR} non trovata.")
        return

    print(f"[*] Scansione integrale di {MODELLO_DIR}...")
    for root, dirs, files in os.walk(MODELLO_DIR):
        for file in files:
            f_path = os.path.join(root, file)
            try:
                # Leggiamo il file come testo
                with open(f_path, 'r', errors='ignore') as f:
                    content = f.read().strip()
                
                if not content: continue

                # Se è un JSONL, estraiamo i campi
                if file.endswith('.jsonl'):
                    for line in content.split('\n'):
                        try:
                            data = json.loads(line)
                            training_data.append({
                                "instruction": data.get("prompt", data.get("istruzione", f"Analisi del file {file}")),
                                "input": data.get("input", data.get("codice", "")),
                                "output": data.get("completion", data.get("risposta", data.get("content", "")))
                            })
                        except: continue
                else:
                    # Per ogni altro file (C, Py, Sh, etc.), creiamo una voce di conoscenza pura
                    training_data.append({
                        "instruction": f"Qual è il contenuto e la logica del file {file}?",
                        "input": f"Percorso: {f_path}",
                        "output": f"CONTENUTO INTEGRALE:\n{content}"
                    })
                
                print(f" [+] Integrato: {file}")
            except Exception as e:
                print(f" [!] Errore su {file}: {e}")

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(training_data, f, indent=4)
    
    print(f"\n[OK] Dataset ATOMICO creato con successo!")
    print(f" > File: {OUTPUT_FILE}")
    print(f" > Totale campioni di addestramento: {len(training_data)}")

if __name__ == "__main__":
    genera_dataset_atomico()
