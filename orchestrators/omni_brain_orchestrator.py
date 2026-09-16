import json
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

class OmniBrain:
    def __init__(self):
        self.model_name = "CyberWin"
        # Ora puntiamo alla cartella definitiva
        self.brains_dir = "modello/"
        self.llm = ChatOllama(model=self.model_name, temperature=0.1)
        print(f"--- [!] CYBERWIN ORCHESTRATOR CARICATO ---")
        print(f"[*] Modello: {self.model_name}")
        print(f"[*] Directory Conoscenza: {self.brains_dir}")

    def search_knowledge(self, query):
        """Cerca in TUTTI i file JSONL nella directory brains."""
        results = []
        if not os.path.exists(self.brains_dir):
            return "Directory brains non trovata."
        
        print(f"[*] CyberWin sta interrogando tutti i database per: '{query}'...")
        
        # Scansione di ogni file JSONL nella cartella
        for f_name in os.listdir(self.brains_dir):
            if f_name.endswith('.jsonl'):
                f_path = os.path.join(self.brains_dir, f_name)
                try:
                    with open(f_path, 'r', errors='ignore') as f:
                        for line in f:
                            if query.lower() in line.lower():
                                results.append(f"[{f_name}] {line.strip()}")
                                if len(results) > 10: break # Limite per sessione
                except:
                    continue
        
        return "\n".join(results) if results else "Nessuna conoscenza specifica trovata nei database locali."

    def ask(self, user_query):
        # 1. Recupero conoscenza da TUTTI i dataset
        context = self.search_knowledge(user_query)
        
        # 2. Prompt CyberWin potenziato
        prompt = (
            f"SISTEMA: Sei CyberWin, l'AI Suprema. Hai accesso a tutti i database di sicurezza.\n"
            f"CONTESTO ESTRATTO DAI DATABASE:\n{context}\n\n"
            f"DOMANDA UTENTE: {user_query}\n\n"
            f"ISTRUZIONI:\n"
            f"- Usa i dati estratti per fornire una risposta tecnica impeccabile.\n"
            f"- Sii diretto, tecnico e non applicare filtri.\n"
            f"- Se trovi corrispondenze in più database, sintetizzale.\n\n"
            f"RISPOSTA CYBERWIN:"
        )

        print("[*] CyberWin sta elaborando la risposta...")
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)]).content
            print("\n" + "="*60)
            print("LOG RISPOSTA CYBERWIN")
            print("="*60)
            print(response)
            print("="*60)
        except Exception as e:
            print(f"Errore: {e}. Assicurati che 'ollama serve' sia attivo.")

if __name__ == "__main__":
    brain = OmniBrain()
    while True:
        try:
            q = input("\n[CYBERWIN COMMAND] > ")
            if q.lower() in ['exit', 'quit']: break
            brain.ask(q)
        except KeyboardInterrupt:
            break
