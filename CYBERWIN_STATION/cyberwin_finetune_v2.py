import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
import os

# 1. Configurazione Quantizzazione
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# 2. Caricamento Modello e Tokenizer
model_id = "NousResearch/Meta-Llama-3-8B-Instruct" 
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# 3. Configurazione LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# 4. Caricamento del Dataset Reale
dataset_path = "modello/dataset_atomico_cyberwin.json"
dataset = load_dataset("json", data_files=dataset_path, split="train")

def format_instruction(sample):
    return f"### Istruzione:\n{sample['instruction']}\n\n### Input:\n{sample['input']}\n\n### Risposta:\n{sample['output']}"

# 5. Configurazione Addestramento
training_args = TrainingArguments(
    output_dir="./CYBERWIN_STATION/risultati_addestramento",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    save_steps=50,
    logging_steps=10,
    fp16=True,
)

# 6. Avvio dell'allenatore (SFT)
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer,
    formatting_func=format_instruction,
)

if __name__ == "__main__":
    print("[*] AVVIO ADDESTRAMENTO DI CYBERWIN V2...")
    trainer.train()
    model.save_pretrained("./CYBERWIN_STATION/cyberwin_final_model")
    print("[OK] Addestramento completato e modello salvato!")
