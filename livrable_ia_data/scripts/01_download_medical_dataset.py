"""
Téléchargement du dataset médical depuis HuggingFace.
Source: ruslanmv/ai-medical-chatbot
"""

from datasets import load_dataset
import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "medical_dataset")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Téléchargement du dataset médical depuis HuggingFace...")
dataset = load_dataset("ruslanmv/ai-medical-chatbot")

print(f"Dataset chargé: {dataset}")
print(f"Nombre d'exemples (train): {len(dataset['train'])}")

if "test" in dataset:
    print(f"Nombre d'exemples (test): {len(dataset['test'])}")

print("\nColonnes disponibles:", dataset["train"].column_names)
print("\nExemple de donnée:")
print(json.dumps(dataset["train"][0], indent=2, ensure_ascii=False))

raw_path = os.path.join(OUTPUT_DIR, "raw_medical_data.json")
dataset["train"].to_json(raw_path)
print(f"\nDataset brut sauvegardé dans: {raw_path}")
print(f"Taille du fichier: {os.path.getsize(raw_path) / (1024*1024):.1f} MB")
