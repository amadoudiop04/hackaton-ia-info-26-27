"""
Fine-tuning LoRA d'un modèle médical expérimental.
Conçu pour Google Colab Pro (GPU T4/A100).
Utilise Unsloth pour un fine-tuning 2x plus rapide avec 60% moins de mémoire.

Usage local:  python 05_finetune_medical_lora.py
Usage Colab:  copier ce script dans un notebook Colab avec GPU activé
"""

import os
import json
import torch
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATASET_DIR = os.path.join(BASE_DIR, "medical_dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "models", "medical_lora")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Configuration ---
CONFIG = {
    "base_model": "unsloth/Phi-3.5-mini-instruct",
    "max_seq_length": 2048,
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "target_modules": [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    "learning_rate": 2e-4,
    "num_epochs": 3,
    "batch_size": 4,
    "gradient_accumulation_steps": 4,
    "warmup_ratio": 0.1,
    "weight_decay": 0.01,
    "max_grad_norm": 1.0,
    "seed": 42,
}


def install_dependencies():
    print("Installation des dépendances...")
    os.system("pip install -q unsloth transformers datasets peft trl accelerate bitsandbytes")


def load_dataset_from_jsonl(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def format_chatml(sample):
    messages = sample["messages"]
    text = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        text += f"<|{role}|>\n{content}<|end|>\n"
    return {"text": text}


def main():
    print("=" * 60)
    print("FINE-TUNING LoRA - MODÈLE MÉDICAL EXPÉRIMENTAL")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Device: {'cuda' if torch.cuda.is_available() else 'cpu'}")

    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_mem / 1024**3:.1f} GB")

    if not torch.cuda.is_available():
        print("\nATTENTION: Pas de GPU détecté. Le fine-tuning sera très lent.")
        print("Recommandation: Utilisez Google Colab Pro avec GPU T4 ou A100.")
        response = input("Continuer quand même? (o/n): ")
        if response.lower() != "o":
            print("Abandon.")
            return

    try:
        from unsloth import FastLanguageModel
    except ImportError:
        print("Unsloth non installé. Installation en cours...")
        install_dependencies()
        from unsloth import FastLanguageModel

    print(f"\nChargement du modèle de base: {CONFIG['base_model']}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=CONFIG["base_model"],
        max_seq_length=CONFIG["max_seq_length"],
        dtype=None,
        load_in_4bit=True,
    )

    print("Application de la configuration LoRA...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=CONFIG["lora_r"],
        target_modules=CONFIG["target_modules"],
        lora_alpha=CONFIG["lora_alpha"],
        lora_dropout=CONFIG["lora_dropout"],
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=CONFIG["seed"],
    )

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Paramètres entraînables: {trainable_params:,} / {total_params:,} ({100 * trainable_params / total_params:.2f}%)")

    train_path = os.path.join(DATASET_DIR, "train_chatml.jsonl")
    val_path = os.path.join(DATASET_DIR, "val_chatml.jsonl")

    print(f"\nChargement du dataset...")
    train_data = load_dataset_from_jsonl(train_path)
    val_data = load_dataset_from_jsonl(val_path)
    print(f"  Train: {len(train_data)} échantillons")
    print(f"  Val: {len(val_data)} échantillons")

    from datasets import Dataset
    train_dataset = Dataset.from_list(train_data).map(format_chatml)
    val_dataset = Dataset.from_list(val_data).map(format_chatml)

    from trl import SFTTrainer
    from transformers import TrainingArguments

    print("\nDémarrage du fine-tuning...")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=CONFIG["num_epochs"],
        per_device_train_batch_size=CONFIG["batch_size"],
        gradient_accumulation_steps=CONFIG["gradient_accumulation_steps"],
        learning_rate=CONFIG["learning_rate"],
        weight_decay=CONFIG["weight_decay"],
        warmup_ratio=CONFIG["warmup_ratio"],
        max_grad_norm=CONFIG["max_grad_norm"],
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=3,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        seed=CONFIG["seed"],
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        args=training_args,
        dataset_text_field="text",
        max_seq_length=CONFIG["max_seq_length"],
    )

    start_time = datetime.now()
    train_result = trainer.train()
    training_time = (datetime.now() - start_time).total_seconds()

    print(f"\nFine-tuning terminé en {training_time / 60:.1f} minutes")
    print(f"  Loss finale: {train_result.training_loss:.4f}")

    lora_path = os.path.join(OUTPUT_DIR, "lora_adapter")
    print(f"\nSauvegarde de l'adaptateur LoRA: {lora_path}")
    model.save_pretrained(lora_path)
    tokenizer.save_pretrained(lora_path)

    training_report = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "base_model": CONFIG["base_model"],
        "config": CONFIG,
        "training_time_minutes": round(training_time / 60, 1),
        "final_loss": round(train_result.training_loss, 4),
        "train_samples": len(train_data),
        "val_samples": len(val_data),
        "trainable_params": trainable_params,
        "total_params": total_params,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
        "output_path": lora_path,
    }

    report_path = os.path.join(OUTPUT_DIR, "training_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(training_report, f, indent=2, ensure_ascii=False)
    print(f"Rapport de training sauvegardé: {report_path}")

    print("\n" + "=" * 60)
    print("FINE-TUNING TERMINÉ AVEC SUCCÈS")
    print(f"Adaptateur LoRA: {lora_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
