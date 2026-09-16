#!/bin/bash
# SETUP AMBIENTE CYBERWIN V1.0

echo "--- CONFIGURAZIONE AMBIENTE VIRTUALE CYBERWIN ---"

# Creazione del venv se non esiste
if [ ! -d "cyber_venv" ]; then
    echo "[*] Creazione ambiente virtuale 'cyber_venv'..."
    python3 -m venv cyber_venv
else
    echo "[*] Ambiente 'cyber_venv' già esistente."
fi

# Upgrade di pip e installazione librerie
echo "[*] Installazione librerie di addestramento..."
./cyber_venv/bin/python -m pip install --upgrade pip
./cyber_venv/bin/python -m pip install datasets transformers peft trl accelerate bitsandbytes torch

echo "--- CONFIGURAZIONE COMPLETATA ---"
echo "[OK] Ora puoi lanciare l'addestramento con:"
echo "./cyber_venv/bin/python CYBERWIN_STATION/cyberwin_finetune_v2.py"
