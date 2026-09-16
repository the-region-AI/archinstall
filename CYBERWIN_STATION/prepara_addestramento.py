import json
import os

BRAINS_DIR = "CYBERWIN_STATION/brains/"
TRAIN_DATASET = "CYBERWIN_STATION/cyberwin_training_final.json"

def prepara_dataset_addestramento():
    print("\n--- PREPARAZIONE DATASET PER FINE-TUNING CYBERWIN ---")
    training_data = []
    
    if not os.path.exists(BRAINS_DIR):
        print("[!] Errore: Cartella brains non trovata.")
        return

    print("[*] Estrazione campioni dai database JSONL...")
    for f_name in os.listdir(BRAINS_DIR):
        if f_name.endswith('.jsonl'):
            f_path = os.path.join(BRAINS_DIR, f_name)
            with open(f_path, 'r', errors='ignore') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        # Convertiamo ogni formato nel formato standard Alpaca/Llama
                        entry = {
                            "instruction": data.get("prompt", data.get("istruzione", "Analizza o genera codice di sicurezza.")),
                            "input": data.get("input", data.get("codice", "")),
                            "output": data.get("completion", data.get("risposta", data.get("content", "")))
                        }
                        if entry["output"]:
                            training_data.append(entry)
                    except:
                        continue
            print(f" > Elaborato: {f_name}")

    with open(TRAIN_DATASET, 'w') as f:
        json.dump(training_data, f, indent=4)
    
    print(f"\n[OK] Dataset pronto per l'addestramento!")
    print(f" > File: {TRAIN_DATASET}")
    print(f" > Totale campioni di addestramento: {len(training_data)}")

if __name__ == "__main__":
    prepara_dataset_addestramento()
