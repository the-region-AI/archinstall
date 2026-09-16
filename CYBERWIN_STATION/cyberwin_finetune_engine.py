
# CYBERWIN FINE-TUNING ENGINE V1.0
# Basato su Unsloth per addestramento ultra-veloce

from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 1. Configurazione Modello
model_name = "unsloth/llama-3-8b-instruct-bnb-4bit" # Base per CyberWin
max_seq_length = 2048

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_length,
    load_in_4bit = True,
)

# 2. Aggiunta dei 'Neuroni' CyberWin (LoRA)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
)

# 3. Caricamento Dataset (I tuoi 72.000 file)
dataset = load_dataset("json", data_files="CYBERWIN_STATION/cyberwin_training_final.json", split="train")

# 4. Avvio Addestramento
trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    dataset_text_field = "output", # O il campo che preferisci
    max_seq_length = max_seq_length,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 60, # Regola in base alla tua GPU
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        output_dir = "outputs",
    ),
)

print("[*] AVVIO ADDESTRAMENTO CYBERWIN...")
trainer.train()

# 5. Esportazione per Ollama
print("[*] ADDESTRAMENTO COMPLETATO. Esportazione in corso...")
model.save_pretrained_gguf("CyberWin-Native", tokenizer, quantization_method = "q4_k_m")
print("[OK] Modello CyberWin-Native pronto per Ollama!")
