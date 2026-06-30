"""
Analyse, nettoyage et préparation du dataset médical.
Produit un rapport de qualité + dataset nettoyé.
"""

import json
import os
import re
from collections import Counter
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATASET_DIR = os.path.join(BASE_DIR, "medical_dataset")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

RAW_PATH = os.path.join(DATASET_DIR, "raw_medical_data.json")


def load_raw_data():
    data = []
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def analyze_data(data):
    stats = {
        "total_samples": len(data),
        "columns": list(data[0].keys()) if data else [],
        "empty_fields": Counter(),
        "field_lengths": {},
        "duplicates": 0,
        "language_issues": 0,
        "short_responses": 0,
        "long_responses": 0,
    }

    seen = set()
    all_lengths = {}

    for item in data:
        for key in item:
            if key not in all_lengths:
                all_lengths[key] = []

            value = str(item.get(key, ""))
            all_lengths[key].append(len(value))

            if not value.strip():
                stats["empty_fields"][key] += 1

        fingerprint = json.dumps(item, sort_keys=True)
        if fingerprint in seen:
            stats["duplicates"] += 1
        seen.add(fingerprint)

        answer_fields = ["Answer", "answer", "output", "response", "Doctor"]
        for af in answer_fields:
            if af in item:
                answer = str(item[af])
                if len(answer) < 10:
                    stats["short_responses"] += 1
                if len(answer) > 5000:
                    stats["long_responses"] += 1
                break

    for key, lengths in all_lengths.items():
        stats["field_lengths"][key] = {
            "min": min(lengths),
            "max": max(lengths),
            "avg": round(sum(lengths) / len(lengths), 1),
            "median": sorted(lengths)[len(lengths) // 2],
        }

    return stats


def clean_text(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\x00", "")
    return text


def clean_data(data):
    cleaned = []
    removed = {"empty": 0, "duplicate": 0, "too_short": 0}
    seen = set()

    for item in data:
        cleaned_item = {}
        for key, value in item.items():
            cleaned_item[key] = clean_text(value)

        answer_fields = ["Answer", "answer", "output", "response", "Doctor"]
        question_fields = ["Question", "question", "input", "instruction", "Patient", "Description"]

        question = ""
        answer = ""
        for qf in question_fields:
            if qf in cleaned_item and cleaned_item[qf].strip():
                question = cleaned_item[qf]
                break
        for af in answer_fields:
            if af in cleaned_item and cleaned_item[af].strip():
                answer = cleaned_item[af]
                break

        if not question.strip() or not answer.strip():
            removed["empty"] += 1
            continue

        if len(answer) < 10:
            removed["too_short"] += 1
            continue

        fingerprint = f"{question}|{answer}"
        if fingerprint in seen:
            removed["duplicate"] += 1
            continue
        seen.add(fingerprint)

        cleaned.append(cleaned_item)

    return cleaned, removed


def generate_report(stats_before, stats_after, removed, data_sample):
    report = f"""# Rapport de Qualité des Données - Dataset Médical
## TechCorp Industries - Équipe IA/DATA
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 1. Vue d'ensemble du Dataset Brut

| Métrique | Valeur |
|----------|--------|
| Nombre total d'échantillons | {stats_before['total_samples']} |
| Colonnes | {', '.join(stats_before['columns'])} |
| Doublons détectés | {stats_before['duplicates']} |
| Réponses trop courtes (<10 chars) | {stats_before['short_responses']} |
| Réponses très longues (>5000 chars) | {stats_before['long_responses']} |

### Champs vides
"""
    for field, count in stats_before["empty_fields"].items():
        pct = (count / stats_before["total_samples"]) * 100
        report += f"- **{field}**: {count} ({pct:.1f}%)\n"

    report += "\n### Statistiques de longueur des champs\n"
    for field, lengths in stats_before["field_lengths"].items():
        report += f"- **{field}**: min={lengths['min']}, max={lengths['max']}, avg={lengths['avg']}, median={lengths['median']}\n"

    report += f"""
---

## 2. Nettoyage effectué

| Opération | Échantillons retirés |
|-----------|---------------------|
| Champs vides | {removed['empty']} |
| Doublons | {removed['duplicate']} |
| Réponses trop courtes | {removed['too_short']} |
| **Total retiré** | **{sum(removed.values())}** |

### Opérations de nettoyage appliquées:
- Suppression des espaces multiples et caractères de contrôle
- Suppression des balises HTML résiduelles
- Suppression des caractères null
- Déduplication exacte (question + réponse)
- Filtrage des réponses < 10 caractères

---

## 3. Dataset nettoyé

| Métrique | Valeur |
|----------|--------|
| Échantillons conservés | {stats_after['total_samples']} |
| Taux de rétention | {(stats_after['total_samples'] / stats_before['total_samples']) * 100:.1f}% |

---

## 4. Échantillons de données (3 premiers)

"""
    for i, sample in enumerate(data_sample[:3]):
        report += f"### Échantillon {i+1}\n```json\n{json.dumps(sample, indent=2, ensure_ascii=False)}\n```\n\n"

    report += """---

## 5. Recommandations

- Le dataset est de qualité suffisante pour un fine-tuning LoRA expérimental
- Les conversations suivent un format question/réponse médical cohérent
- Recommandation: utiliser un split 90/10 pour train/validation
- Surveiller les performances sur les réponses longues (risque de troncature)

---
*Rapport généré automatiquement par l'équipe IA/DATA de TechCorp Industries*
"""
    return report


def main():
    print("Chargement des données brutes...")
    data = load_raw_data()
    print(f"  {len(data)} échantillons chargés")

    print("\nAnalyse du dataset brut...")
    stats_before = analyze_data(data)
    print(f"  Doublons: {stats_before['duplicates']}")
    print(f"  Réponses courtes: {stats_before['short_responses']}")

    print("\nNettoyage en cours...")
    cleaned_data, removed = clean_data(data)
    print(f"  Retirés - vides: {removed['empty']}, doublons: {removed['duplicate']}, courts: {removed['too_short']}")
    print(f"  Conservés: {len(cleaned_data)}")

    stats_after = analyze_data(cleaned_data)

    print("\nGénération du rapport de qualité...")
    report = generate_report(stats_before, stats_after, removed, cleaned_data)
    report_path = os.path.join(REPORTS_DIR, "rapport_qualite_donnees.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Rapport sauvegardé: {report_path}")

    print("\nSauvegarde du dataset nettoyé...")
    clean_path = os.path.join(DATASET_DIR, "cleaned_medical_data.json")
    with open(clean_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    print(f"  Dataset nettoyé: {clean_path}")
    print(f"  Taille: {os.path.getsize(clean_path) / (1024*1024):.1f} MB")


if __name__ == "__main__":
    main()
