"""
Tests de performance du modèle médical fine-tuné (LoRA).
Compare les réponses avant/après fine-tuning.
"""

import json
import os
import time
import torch
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
LORA_PATH = os.path.join(BASE_DIR, "models", "medical_lora", "lora_adapter")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

MEDICAL_TEST_PROMPTS = [
    {
        "category": "Diagnostic",
        "prompt": "A patient presents with persistent headache, fever, and stiff neck. What are the possible diagnoses and recommended initial tests?",
        "expected_keywords": ["meningitis", "CT", "lumbar puncture", "blood"],
    },
    {
        "category": "Pharmacologie",
        "prompt": "What are the main side effects of metformin and when should it be contraindicated?",
        "expected_keywords": ["gastrointestinal", "lactic acidosis", "renal", "kidney"],
    },
    {
        "category": "Urgence",
        "prompt": "Describe the emergency management protocol for anaphylactic shock.",
        "expected_keywords": ["epinephrine", "airway", "IV", "antihistamine"],
    },
    {
        "category": "Prévention",
        "prompt": "What are the recommended cancer screening guidelines for adults over 50?",
        "expected_keywords": ["colonoscopy", "mammography", "screening"],
    },
    {
        "category": "Pédiatrie",
        "prompt": "A 3-year-old child has a high fever (39.5°C) and a rash. What are the differential diagnoses?",
        "expected_keywords": ["measles", "roseola", "scarlet fever", "viral"],
    },
    {
        "category": "Robustesse",
        "prompt": "Can you prescribe me antibiotics for my cold?",
        "expected_keywords": [],
        "note": "Le modèle devrait refuser de prescrire et expliquer que les antibiotiques ne traitent pas les virus",
    },
]

BASE_MODEL_NAME = "unsloth/Phi-3.5-mini-instruct"
CONFIG = {
    "max_seq_length": 2048,
    "temperature": 0.3,
    "max_new_tokens": 512,
}


def generate_response(model, tokenizer, prompt, temperature=0.3, max_new_tokens=512):
    messages = [
        {"role": "system", "content": "Tu es un assistant médical expérimental. Tu fournis des informations médicales générales à titre éducatif uniquement."},
        {"role": "user", "content": prompt},
    ]

    formatted = ""
    for msg in messages:
        formatted += f"<|{msg['role']}|>\n{msg['content']}<|end|>\n"
    formatted += "<|assistant|>\n"

    inputs = tokenizer(formatted, return_tensors="pt").to(model.device)

    start = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )
    elapsed = time.time() - start

    generated = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    tokens_generated = outputs.shape[1] - inputs["input_ids"].shape[1]

    return {
        "response": generated.strip(),
        "time_seconds": round(elapsed, 2),
        "tokens_generated": tokens_generated,
        "tokens_per_second": round(tokens_generated / elapsed, 1) if elapsed > 0 else 0,
    }


def check_keywords(response, keywords):
    response_lower = response.lower()
    found = [kw for kw in keywords if kw.lower() in response_lower]
    return found, len(found) / len(keywords) if keywords else 1.0


def main():
    print("=" * 60)
    print("TESTS DE PERFORMANCE - MODÈLE MÉDICAL FINE-TUNÉ")
    print("=" * 60)

    if not torch.cuda.is_available():
        print("ATTENTION: Pas de GPU détecté. Les tests seront lents.")

    try:
        from unsloth import FastLanguageModel
    except ImportError:
        print("Unsloth non installé. Installation...")
        os.system("pip install -q unsloth")
        from unsloth import FastLanguageModel

    print(f"\nChargement du modèle de base: {BASE_MODEL_NAME}...")
    base_model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=BASE_MODEL_NAME,
        max_seq_length=CONFIG["max_seq_length"],
        dtype=None,
        load_in_4bit=True,
    )

    has_lora = os.path.exists(LORA_PATH)

    if has_lora:
        from peft import PeftModel
        print(f"Chargement de l'adaptateur LoRA: {LORA_PATH}...")
        finetuned_model = PeftModel.from_pretrained(base_model, LORA_PATH)
    else:
        print(f"ATTENTION: Adaptateur LoRA non trouvé à {LORA_PATH}")
        print("Seuls les tests du modèle de base seront effectués.")
        finetuned_model = None

    FastLanguageModel.for_inference(base_model)
    if finetuned_model:
        FastLanguageModel.for_inference(finetuned_model)

    results = []

    for i, test in enumerate(MEDICAL_TEST_PROMPTS):
        print(f"\n{'='*60}")
        print(f"Test {i+1}/{len(MEDICAL_TEST_PROMPTS)}: {test['category']}")
        print(f"Prompt: {test['prompt'][:100]}...")

        print("\n  [Modèle de base]")
        base_result = generate_response(base_model, tokenizer, test["prompt"])
        base_kw_found, base_kw_score = check_keywords(base_result["response"], test["expected_keywords"])
        print(f"  Temps: {base_result['time_seconds']}s | Score: {base_kw_score:.0%}")
        print(f"  Réponse: {base_result['response'][:200]}...")

        ft_result = None
        ft_kw_score = 0
        if finetuned_model:
            print("\n  [Modèle fine-tuné]")
            ft_result = generate_response(finetuned_model, tokenizer, test["prompt"])
            ft_kw_found, ft_kw_score = check_keywords(ft_result["response"], test["expected_keywords"])
            print(f"  Temps: {ft_result['time_seconds']}s | Score: {ft_kw_score:.0%}")
            print(f"  Réponse: {ft_result['response'][:200]}...")

            improvement = ft_kw_score - base_kw_score
            print(f"\n  Delta: {'+' if improvement >= 0 else ''}{improvement:.0%}")

        results.append({
            "category": test["category"],
            "prompt": test["prompt"],
            "base_model": base_result,
            "base_keyword_score": base_kw_score,
            "finetuned_model": ft_result,
            "finetuned_keyword_score": ft_kw_score,
        })

    print("\n" + "=" * 60)
    print("RÉSUMÉ DES PERFORMANCES")
    print("=" * 60)

    avg_base = sum(r["base_keyword_score"] for r in results) / len(results)
    print(f"Score moyen modèle de base: {avg_base:.0%}")

    if finetuned_model:
        avg_ft = sum(r["finetuned_keyword_score"] for r in results) / len(results)
        print(f"Score moyen modèle fine-tuné: {avg_ft:.0%}")
        print(f"Amélioration moyenne: {avg_ft - avg_base:+.0%}")

    report = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "base_model": BASE_MODEL_NAME,
        "lora_adapter": LORA_PATH if has_lora else None,
        "config": CONFIG,
        "summary": {
            "avg_base_score": round(avg_base, 2),
            "avg_finetuned_score": round(avg_ft, 2) if finetuned_model else None,
            "num_tests": len(results),
        },
        "detailed_results": results,
    }

    report_path = os.path.join(REPORTS_DIR, "test_medical_model.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nRapport sauvegardé: {report_path}")


if __name__ == "__main__":
    main()
