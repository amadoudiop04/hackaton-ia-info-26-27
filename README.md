# DEV WEB — Interface Chat TechCorp

Interface web de chat (Streamlit) connectée au serveur d'inférence de l'équipe INFRA
(Ollama par défaut : `http://localhost:11434`) pour dialoguer avec le modèle
**Phi-3.5-Financial**.

## Architecture

```
web/
├── app.py                  # Point d'entrée Streamlit (orchestration UI)
├── config.py               # Configuration centralisée (URL serveur, modèle, params)
├── requirements.txt        # Dépendances Python (streamlit, requests)
├── .env.example            # Variables d'environnement (à copier en .env)
│
├── .streamlit/
│   └── config.toml         # Thème + réglages serveur Streamlit
│
├── services/
│   ├── __init__.py
│   └── inference.py        # Client serveur d'inférence (Ollama / API REST)
│
├── components/
│   ├── __init__.py
│   ├── chat.py             # Rendu de la conversation + saisie utilisateur
│   └── sidebar.py          # Panneau de paramètres (modèle, température…)
│
├── utils/
│   ├── __init__.py
│   └── history.py          # Gestion de l'historique de conversation (session_state)
│
└── assets/
    └── style.css           # Styles personnalisés de l'interface
```

## Démarrage

```bash
cd web
pip install -r requirements.txt
cp .env.example .env        # ajuster OLLAMA_URL / MODEL_NAME si besoin
streamlit run app.py
```

L'interface est disponible sur http://localhost:8501

## Intégration serveur d'inférence

| Serveur        | URL par défaut            |
|----------------|---------------------------|
| Ollama         | http://localhost:11434    |
| Triton         | http://localhost:8000     |
| Serveur maison | communiquée par l'INFRA   |

Le point d'intégration unique est [services/inference.py](services/inference.py) :
changer de backend = adapter ce seul module.
