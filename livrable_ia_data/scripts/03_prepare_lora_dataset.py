"""
Préparation du dataset médical au format requis pour le fine-tuning LoRA.
Convertit les conversations en format instruction/input/output compatible avec les frameworks de fine-tuning.
"""

import json
import os
import random

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATASET_DIR = os.path.join(BASE_DIR, "medical_dataset")
CLEAN_PATH = os.path.join(DATASET_DIR, "cleaned_medical_data.json")

SYSTEM_PROMPT = (
    "Tu es un assistant médical expérimental. Tu fournis des informations médicales "
    "générales à titre éducatif uniquement. Tu ne remplaces pas un avis médical professionnel. "
    "Consulte toujours un professionnel de santé pour tout problème médical."
)

TRAIN_RATIO = 0.9


def detect_fields(sample):
    question_candidates = ["Patient", "Question", "question", "input", "instruction", "Description"]
    answer_candidates = ["Doctor", "Answer", "answer", "output", "response"]

    q_field = None
    a_field = None

    for qf in question_candidates:
        if qf in sample:
            q_field = qf
            break

    for af in answer_candidates:
        if af in sample:
            a_field = af
            break

    return q_field, a_field


def convert_to_chatml(data, q_field, a_field):
    """Format ChatML pour fine-tuning avec transformers/unsloth."""
    formatted = []
    for item in data:
        question = str(item.get(q_field, "")).strip()
        answer = str(item.get(a_field, "")).strip()

        if not question or not answer:
            continue

        conversation = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer},
            ]
        }
        formatted.append(conversation)

    return formatted


def convert_to_alpaca(data, q_field, a_field):
    """Format Alpaca pour fine-tuning classique."""
    formatted = []
    for item in data:
        question = str(item.get(q_field, "")).strip()
        answer = str(item.get(a_field, "")).strip()

        if not question or not answer:
            continue

        entry = {
            "instruction": "Réponds à la question médicale suivante de manière professionnelle et détaillée.",
            "input": question,
            "output": answer,
        }
        formatted.append(entry)

    return formatted


def split_dataset(data, train_ratio=TRAIN_RATIO):
    random.seed(42)
    shuffled = data.copy()
    random.shuffle(shuffled)
    split_idx = int(len(shuffled) * train_ratio)
    return shuffled[:split_idx], shuffled[split_idx:]


def save_jsonl(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    print("Chargement du dataset nettoyé...")
    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  {len(data)} échantillons chargés")

    q_field, a_field = detect_fields(data[0])
    print(f"  Champs détectés - Question: '{q_field}', Réponse: '{a_field}'")

    print("\nConversion au format ChatML...")
    chatml_data = convert_to_chatml(data, q_field, a_field)
    print(f"  {len(chatml_data)} conversations formatées")

    print("\nConversion au format Alpaca...")
    alpaca_data = convert_to_alpaca(data, q_field, a_field)
    print(f"  {len(alpaca_data)} entrées formatées")

    print(f"\nSplit train/val ({TRAIN_RATIO:.0%}/{1-TRAIN_RATIO:.0%})...")
    chatml_train, chatml_val = split_dataset(chatml_data)
    alpaca_train, alpaca_val = split_dataset(alpaca_data)
    print(f"  Train: {len(chatml_train)}, Val: {len(chatml_val)}")

    print("\nSauvegarde des fichiers...")

    save_jsonl(chatml_train, os.path.join(DATASET_DIR, "train_chatml.jsonl"))
    save_jsonl(chatml_val, os.path.join(DATASET_DIR, "val_chatml.jsonl"))
    print("  Format ChatML: train_chatml.jsonl, val_chatml.jsonl")

    save_jsonl(alpaca_train, os.path.join(DATASET_DIR, "train_alpaca.jsonl"))
    save_jsonl(alpaca_val, os.path.join(DATASET_DIR, "val_alpaca.jsonl"))
    print("  Format Alpaca: train_alpaca.jsonl, val_alpaca.jsonl")

    print("\nExemple ChatML:")
    print(json.dumps(chatml_data[0], indent=2, ensure_ascii=False))

    print("\nExemple Alpaca:")
    print(json.dumps(alpaca_data[0], indent=2, ensure_ascii=False))

    print("\nDataset prêt pour le fine-tuning LoRA!")


if __name__ == "__main__":
    main()
