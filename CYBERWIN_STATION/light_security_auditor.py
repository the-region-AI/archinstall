import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import os

# CONFIGURAZIONE ANALISTA DIFENSIVO LEGGERO (CYBERWIN DEFENDER)
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

def inizializza_analista():
    print(f"[*] Caricamento dell'Analista Difensivo: {model_id}...")
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
    return model, tokenizer

def analizza_vulnerabilita(file_path, model, tokenizer):
    if not os.path.exists(file_path):
        return f"Errore: Il file {file_path} non esiste."

    with open(file_path, "r") as f:
        code = f.read()

    print(f"[*] Analisi difensiva in corso su: {file_path}")
    
    # Prompt focalizzato esclusivamente sulla difesa e sulla correzione
    prompt = (
        f"<|system|>\nSei un esperto di cybersecurity difensiva e auditing. "
        f"Il tuo compito è identificare vulnerabilità nel codice e fornire la soluzione (patch) per risolverle.</s>\n"
        f"<|user|>\nAnalizza questo codice e suggerisci le correzioni di sicurezza:\n\n{code}</s>\n"
        f"<|assistant|>\n"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.1, do_sample=True)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Testiamo l'analista su uno script vulnerabile per scopi di protezione
    model, tokenizer = inizializza_analista()
    target = "vulnerable_rce.py"
    report = analizza_vulnerabilita(target, model, tokenizer)
    
    print("\n" + "="*60)
    print("REPORT DI SICUREZZA DIFENSIVA - CYBERWIN")
    print("="*60)
    print(report)
    print("="*60)
