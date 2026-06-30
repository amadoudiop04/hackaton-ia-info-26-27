# Documentation Technique — Équipe IA/DATA
## TechCorp Industries — Challenge IA

---

## 1. Architecture IA/DATA

```
Arkathon/
├── medical_dataset/           # Données médicales
│   ├── raw_medical_data.json  # Dataset brut (HuggingFace)
│   ├── cleaned_medical_data.json  # Dataset nettoyé
│   ├── train_chatml.jsonl     # Format ChatML (train)
│   ├── val_chatml.jsonl       # Format ChatML (validation)
│   ├── train_alpaca.jsonl     # Format Alpaca (train)
│   └── val_alpaca.jsonl       # Format Alpaca (validation)
├── models/
│   ├── phi3_financial/        # Modèle Phi-3.5-Financial
│   └── medical_lora/          # Adaptateur LoRA médical
│       └── lora_adapter/
├── scripts/
│   ├── 01_download_medical_dataset.py
│   ├── 02_analyze_and_clean_dataset.py
│   ├── 03_prepare_lora_dataset.py
│   ├── 04_validate_phi3_financial.py
│   ├── 05_finetune_medical_lora.py
│   └── 06_test_medical_model.py
├── notebooks/
│   └── finetune_medical_colab.ipynb  # Notebook Colab
├── reports/
│   ├── rapport_qualite_donnees.md
│   ├── validation_phi3_financial.json
│   └── test_medical_model.json
└── requirements.txt
```

---

## 2. Pipeline DATA — Préparation du Dataset Médical

### Source des données
- **Dataset:** `ruslanmv/ai-medical-chatbot` (HuggingFace)
- **Contenu:** Conversations médicales patient/docteur
- **Format:** JSON avec champs Patient/Doctor (ou variantes)

### Processus de nettoyage
1. **Téléchargement** (`01_download_medical_dataset.py`)
   - Récupération depuis HuggingFace Datasets
   - Sauvegarde brute en JSON

2. **Analyse et nettoyage** (`02_analyze_and_clean_dataset.py`)
   - Détection et suppression des doublons
   - Nettoyage des caractères spéciaux et balises HTML
   - Filtrage des réponses trop courtes (<10 caractères)
   - Suppression des entrées avec champs vides
   - Génération du rapport de qualité

3. **Préparation pour fine-tuning** (`03_prepare_lora_dataset.py`)
   - Conversion au format ChatML (messages system/user/assistant)
   - Conversion au format Alpaca (instruction/input/output)
   - Split train/validation (90/10, seed=42)
   - Sauvegarde en JSONL

### Format ChatML (utilisé pour le fine-tuning)
```json
{
  "messages": [
    {"role": "system", "content": "Tu es un assistant médical expérimental..."},
    {"role": "user", "content": "<question du patient>"},
    {"role": "assistant", "content": "<réponse du docteur>"}
  ]
}
```

---

## 3. Pipeline IA — Validation Phi-3.5-Financial

### Script de validation (`04_validate_phi3_financial.py`)
- **Phase 1 — Tests fonctionnels:** 8 prompts couvrant analyse financière, risque, marchés, comptabilité, investissement, fintech + 2 tests de robustesse
- **Phase 2 — Optimisation des paramètres:** Comparaison de 3 configurations (température 0.1, 0.5, 0.8)
- **Métriques:** Temps de réponse, tokens/seconde, score de mots-clés attendus

### Paramètres recommandés
| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| temperature | 0.5 | Équilibre précision/diversité pour la finance |
| top_p | 0.9 | Filtrage des tokens peu probables |
| max_tokens | 512 | Suffisant pour des réponses détaillées |

---

## 4. Pipeline IA — Fine-tuning LoRA Médical

### Configuration LoRA
| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| Modèle de base | Phi-3.5-mini-instruct | Petit, performant, compatible LoRA |
| LoRA rank (r) | 16 | Bon compromis capacité/efficacité |
| LoRA alpha | 32 | Alpha = 2*r, standard |
| Dropout | 0.05 | Régularisation légère |
| Target modules | q,k,v,o,gate,up,down_proj | Couverture complète des couches d'attention + FFN |
| Quantization | 4-bit (QLoRA) | Réduit la VRAM nécessaire de ~70% |

### Hyperparamètres d'entraînement
| Paramètre | Valeur |
|-----------|--------|
| Learning rate | 2e-4 |
| Epochs | 3 |
| Batch size | 4 |
| Gradient accumulation | 4 (batch effectif = 16) |
| Warmup ratio | 10% |
| Weight decay | 0.01 |
| Precision | bf16 (si supporté, sinon fp16) |

### Environnement recommandé
- **Google Colab Pro** avec GPU T4 (16 GB VRAM) ou A100 (40 GB VRAM)
- Temps estimé: ~30-60 min (T4), ~15-30 min (A100)
- Le notebook `finetune_medical_colab.ipynb` est prêt à l'emploi

---

## 5. Tests de performance du modèle médical

### Script de tests (`06_test_medical_model.py`)
- Comparaison avant/après fine-tuning sur 6 prompts médicaux
- Catégories testées: diagnostic, pharmacologie, urgence, prévention, pédiatrie, robustesse
- Métriques: score de mots-clés, temps de réponse, tokens/seconde

### Test de robustesse
- Vérification que le modèle refuse de prescrire
- Vérification que le modèle redirige vers un professionnel de santé

---

## 6. Instructions d'exécution

### Prérequis
```bash
cd Arkathon
pip install -r requirements.txt
```

### Exécution séquentielle (DATA puis IA)
```bash
# DATA: Téléchargement et préparation du dataset
python scripts/01_download_medical_dataset.py
python scripts/02_analyze_and_clean_dataset.py
python scripts/03_prepare_lora_dataset.py

# IA: Validation du modèle financier (nécessite Ollama lancé)
python scripts/04_validate_phi3_financial.py

# IA: Fine-tuning LoRA (nécessite GPU — utiliser Colab de préférence)
python scripts/05_finetune_medical_lora.py

# IA: Tests de performance (nécessite GPU)
python scripts/06_test_medical_model.py
```

### Alternative Colab (recommandée pour le fine-tuning)
1. Uploader `notebooks/finetune_medical_colab.ipynb` sur Google Colab
2. Activer le GPU: Runtime > Change runtime type > T4 GPU
3. Exécuter toutes les cellules
4. Télécharger `medical_lora_adapter.zip` à la fin

---

## 7. Avertissement

Le modèle médical fine-tuné est **expérimental** et destiné uniquement à des fins éducatives et de recherche. Il ne doit en aucun cas être utilisé pour du diagnostic ou des recommandations médicales réelles. Consultez toujours un professionnel de santé qualifié.

---

*Documentation rédigée par l'équipe IA/DATA — TechCorp Industries*
