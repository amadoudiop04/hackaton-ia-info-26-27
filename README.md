<div align="center">

# 💹 TechCorp AI Chat — Assistant Financier Phi-3.5

**Plateforme conversationnelle de bout en bout pour déployer, servir et interroger
le modèle `Phi-3.5-Financial` via une interface web temps réel.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-inference-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-Educational-lightgrey)](#-licence)

</div>

---

## 📖 Sommaire

- [Présentation](#-présentation)
- [Architecture](#-architecture)
- [Structure du dépôt](#-structure-du-dépôt)
- [Prérequis](#-prérequis)
- [Démarrage rapide](#-démarrage-rapide)
  - [1. Serveur d'inférence (Ollama)](#1-serveur-dinférence--ollama)
  - [2. Backend API (FastAPI)](#2-backend-api--fastapi)
  - [3. Frontend (React + Vite)](#3-frontend--react--vite)
  - [Alternative : interface Streamlit](#alternative--interface-streamlit)
- [Contrat d'API](#-contrat-dapi)
- [Configuration](#-configuration)
- [Composants avancés](#-composants-avancés)
- [Volet R&D — Fine-tuning médical](#-volet-rd--fine-tuning-médical)
- [Sécurité](#-sécurité)
- [Feuille de route & rôles](#-feuille-de-route--rôles)
- [Licence](#-licence)

---

## 🎯 Présentation

**TechCorp AI Chat** met à disposition des analystes financiers un assistant
conversationnel basé sur **Phi-3.5-Financial**, un modèle spécialisé finance/business.
Le projet couvre l'ensemble de la chaîne de valeur :

| Domaine | Livrable |
|--------|----------|
| 🏗️ **Infrastructure** | Serveur d'inférence (Ollama, ou Triton en option) servant le modèle |
| 🌐 **Application web** | Backend FastAPI + frontend React, chat temps réel avec streaming |
| 🔬 **R&D** | Pipeline de fine-tuning LoRA pour un modèle médical expérimental |
| 🔒 **Sécurité** | Audit de l'héritage technique (code, logs, datasets) |

L'architecture est **découplée** : le frontend ne dialogue **jamais** directement avec
le serveur d'inférence, mais passe systématiquement par le backend. Changer de moteur
d'inférence (Ollama → Triton → serveur maison) ne demande de modifier qu'**un seul module**.

---

## 🏛️ Architecture

```
┌────────────┐      HTTP/JSON      ┌────────────────┐      HTTP/JSON      ┌──────────────┐
│  Navigateur │ ───────────────────▶│ Frontend React │ ───────────────────▶│  Backend     │
│             │ ◀───────────────────│   (Vite :5173) │ ◀───────────────────│  FastAPI     │
└────────────┘   streaming tokens   └────────────────┘                     │  (:8000)     │
                                                                            └──────┬───────┘
                                                                                   │ httpx
                                                                                   ▼
                                                                       ┌────────────────────┐
                                                                       │  Serveur d'inférence │
                                                                       │  Ollama (:11434)     │
                                                                       │  └─ Phi-3.5-Financial │
                                                                       └────────────────────┘
```

**Principe clé :** le module [`web/backend/services/ollama.py`](web/backend/services/ollama.py)
est le **point d'intégration unique** avec l'infrastructure d'inférence. Le frontend ne
connaît que le contrat HTTP du backend.

---

## 📂 Structure du dépôt

```
hackaton-ia-info-26-27/
├── web/                          # 🌐 Application de chat (livrable principal)
│   ├── backend/                  # API FastAPI
│   │   ├── main.py               #   app + CORS + montage des routes
│   │   ├── config.py             #   settings via pydantic-settings (.env)
│   │   ├── routes/chat.py        #   POST /api/chat · /chat/stream · GET /health
│   │   ├── services/ollama.py    #   client Ollama (httpx) — point d'intégration INFRA
│   │   ├── models/schemas.py     #   ★ contrat Pydantic partagé
│   │   └── requirements.txt
│   ├── frontend/                 # SPA React + Vite + TypeScript
│   │   └── src/
│   │       ├── api/client.ts     #   appelle le BACKEND (jamais Ollama)
│   │       ├── hooks/useChat.ts  #   état conversation + envoi
│   │       ├── components/        #   ChatWindow · Message · ChatInput · Sidebar
│   │       ├── types/chat.ts     #   ★ types alignés sur schemas.py
│   │       └── styles/            #   global · chat · sidebar (.css)
│   └── streamlit/                # Interface alternative mono-fichier (Streamlit)
│
├── ollama_server/                # 🏗️ Modelfile Ollama (Phi-3.5 + prompt système finance)
├── tritton_server/               # 🏗️ Dockerfile Triton Inference Server (déploiement avancé)
├── model_repository/             #     Backend Python Triton + config.pbtxt
├── models/phi3_financial/        # 🤖 Artefacts du modèle (chat template, training args)
│
├── scripts/                      # 🤖 Scripts IA
│   ├── train_finance_model.py    #   fine-tuning LoRA 4-bit (Phi-3-mini)
│   ├── simple_chat.py            #   CLI de test du modèle fine-tuné
│   └── requirements.txt
│
├── medical_project/              # 🔬 Documentation R&D fine-tuning médical
├── datasets/                     # 📊 Datasets (financier / médical — non versionnés)
├── logs/                         # 🔒 Logs hérités (audit sécurité)
│
├── CONSIGNES.md                  # Consignes par filière
├── TASKS.md                      # Découpage des tâches DEV WEB
└── readme.md                     # Ce fichier
```

---

## ✅ Prérequis

| Outil | Version | Usage |
|-------|---------|-------|
| [Ollama](https://ollama.com/download) | dernière | Serveur d'inférence |
| Python | ≥ 3.10 | Backend FastAPI / scripts IA |
| Node.js | ≥ 18 | Frontend React + Vite |
| (option) Docker + GPU NVIDIA | — | Déploiement Triton |

---

## 🚀 Démarrage rapide

> Trois terminaux : **Ollama**, **backend**, **frontend**.

### 1. Serveur d'inférence — Ollama

```bash
# Installer Ollama puis créer le modèle depuis le Modelfile fourni
ollama create phi3.5-financial -f ollama_server/Modelfile
ollama serve          # écoute sur http://localhost:11434
```

Vérification : `curl http://localhost:11434/api/tags` doit lister `phi3.5-financial`.

### 2. Backend API — FastAPI

```bash
cd web/backend
python -m venv .venv && source .venv/Scripts/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

📚 Documentation interactive (Swagger) : <http://localhost:8000/docs>

### 3. Frontend — React + Vite

```bash
cd web/frontend
npm install
cp .env.example .env
npm run dev           # interface sur http://localhost:5173
```

### Alternative : interface Streamlit

Interface mono-fichier, sans build, qui parle directement à Ollama :

```bash
cd web/streamlit
python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

---

## 📜 Contrat d'API

Frontière **backend ↔ frontend**. Les types TypeScript
([`frontend/src/types/chat.ts`](web/frontend/src/types/chat.ts)) restent **alignés** sur
les schémas Pydantic ([`backend/models/schemas.py`](web/backend/models/schemas.py)).

| Méthode | Endpoint | Corps | Réponse |
|---------|----------|-------|---------|
| `POST` | `/api/chat` | `{ messages, temperature?, max_tokens?, model? }` | `{ role, content }` |
| `POST` | `/api/chat/stream` | *(idem)* | flux de tokens `text/plain` |
| `GET` | `/api/health` | — | `{ ok, model }` |

```ts
type Role = "user" | "assistant" | "system";
type Message = { role: Role; content: string };
```

---

## ⚙️ Configuration

Chaque composant lit sa configuration depuis un `.env` (modèle dans `.env.example`).
Les secrets ne sont **jamais** versionnés (`*.env` est ignoré, sauf `.env.example`).

**Backend** ([`web/backend/.env.example`](web/backend/.env.example))

| Variable | Défaut | Description |
|----------|--------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | URL du serveur d'inférence |
| `MODEL_NAME` | `phi3.5-financial` | Nom du modèle Ollama |
| `TEMPERATURE` | `0.7` | Créativité par défaut |
| `MAX_TOKENS` | `512` | Longueur max de réponse (`num_predict`) |
| `REQUEST_TIMEOUT` | `120` | Timeout (s) des requêtes d'inférence |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | Origine autorisée (CORS) |

**Frontend** ([`web/frontend/.env.example`](web/frontend/.env.example))

| Variable | Défaut | Description |
|----------|--------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | URL du backend FastAPI |

---

## 🧩 Composants avancés

### Triton Inference Server (option INFRA)

Pour un déploiement production GPU, une configuration Triton est fournie :

- [`tritton_server/Dockerfile`](tritton_server/Dockerfile) — image basée sur
  `nvcr.io/nvidia/tritonserver` + dépendances Transformers.
- [`model_repository/phi35_financial/`](model_repository/) — backend Python Triton
  ([`model.py`](model_repository/phi35_financial/1/model.py)) et
  [`config.pbtxt`](model_repository/phi35_financial/config.pbtxt) exposant
  `text_input` → `text_output`.

Le backend FastAPI peut basculer vers Triton en adaptant le seul module
[`services/ollama.py`](web/backend/services/ollama.py).

---

## 🔬 Volet R&D — Fine-tuning médical

Pipeline expérimental (non destiné à la production) de fine-tuning **LoRA 4-bit** :

- [`scripts/train_finance_model.py`](scripts/train_finance_model.py) — entraînement
  PEFT/LoRA sur `Phi-3-mini` avec quantization `bitsandbytes` (4-bit nf4).
- [`scripts/simple_chat.py`](scripts/simple_chat.py) — CLI de test du modèle entraîné.
- [`medical_project/Readme.md`](medical_project/Readme.md) — guide méthodologique
  (datasets, QLoRA, optimisation mémoire, considérations RGPD).

```bash
cd scripts
pip install -r requirements.txt
python train_finance_model.py ../datasets/finance_dataset_final.json
```

> ⚠️ Le modèle médical reste **expérimental** : validation par des professionnels de
> santé obligatoire, jamais en substitut d'une expertise humaine.

---

## 🔒 Sécurité

Ce dépôt reprend l'héritage d'une équipe précédente. Le dossier [`logs/`](logs/) contient
des **journaux d'audit** (`training.log`, archives d'équipe) à examiner dans le cadre du
volet sécurité — ils peuvent révéler des anomalies d'entraînement, des contenus injectés
dans le dataset ou des comportements suspects du modèle.

**Bonnes pratiques appliquées :**

- Secrets isolés dans des `.env` non versionnés.
- Frontend découplé du moteur d'inférence (surface d'attaque réduite).
- CORS restreint à l'origine du frontend.
- Gestion d'erreurs propre côté backend (502 si l'inférence est injoignable).

> 🛡️ Avant tout déploiement en production : auditer le modèle (prompt injection, fuite de
> données sensibles, déclencheurs cachés) et valider l'intégrité du dataset de fine-tuning.

---

## 🗺️ Feuille de route & rôles

Le découpage détaillé des tâches DEV WEB est dans [`TASKS.md`](TASKS.md), les consignes
par filière (INFRA, IA, DATA, CYBER, DEV WEB) dans [`CONSIGNES.md`](CONSIGNES.md).

| Filière | Mission |
|---------|---------|
| 🏗️ INFRA | Déployer et exposer le serveur d'inférence |
| 🤖 IA | Valider Phi-3.5-Financial + fine-tuning médical |
| 📊 DATA | Analyser et nettoyer les datasets hérités |
| 🔒 CYBER | Auditer code, logs et données |
| 🌐 DEV WEB | Interface de chat temps réel (backend + frontend) |

---

## 📄 Licence

Projet réalisé dans un cadre **pédagogique** (Challenge IA — TechCorp Industries).
Le code du backend Triton dérive des
[tutoriels NVIDIA Triton](https://github.com/triton-inference-server/tutorials) (licence BSD).

<div align="center">

**TechCorp Industries** · Assistant financier Phi-3.5 · 2026

</div>
