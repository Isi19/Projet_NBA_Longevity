# 🏀 NBA Longevity Prediction API

Ce projet implémente un modèle de **machine learning** permettant de prédire si un joueur NBA jouera **au moins 5 saisons** dans la ligue à partir de ses statistiques de saison rookie.

Il s’agit d’un travail complet de data science comprenant :
- l’analyse exploratoire (EDA)
- la préparation et le feature engineering
- la modélisation
- et une **API FastAPI** pour exposer le modèle en ligne

J'ai choisi une libbrairie FastAPI car c'est plus simple et je propose une solution claire et simple aussi.

---

## Structure du projet

```
ProjetNBADATA/
│
├── app/
│   ├── __init__.py
│   ├── app.py                ← API principale FastAPI
│   ├── player.py             ← Schéma Pydantic (entrée utilisateur)
│   ├── streamilit.py         ← Streamilit UI
│   ├── preprocess.py         ← Fonctions de préparation des données
│
├── data/
|   ├──nba_logreg.csv         ← fichier csv contenat les données des joueurs rookies
|
├── nba_analysis.ipynb        ← Notebook contenant l'analyse exploratoireet la modlisation des ddonnées
├── nba_final_model.pkl       ← Modèle ML entraîné
├── feature_list_final.json   ← Liste ordonnée des features utilisées
├── scaler.pkl                ← Scaler 
├── requirements.txt          ← Dépendances Python
└── README.md                 ← Ce fichier décrit comment utiliser lanceer le web
```

---

##  Lancer l’application

###  Prérequis
 
- Tous les fichiers `.pkl` et `.json` doivent être placés **à la racine de `nba_project/`**

---

###  Étapes d’installation

1️ **Ouvre un terminal** et place-toi dans le dossier racine du projet :

2️ **Installe les dépendances nécessaires** :

```bash
pip install -r requirements.txt
```
---

###  Démarrer le serveur

Une fois dans le dossier `nba_project/`, exécute :

```bash
python -m uvicorn app.app:app --reload
```

>  **Important :**
> - Il faut **impérativement** se placer dans le dossier `nba_project/` avant de lancer la commande.

Si tout est correct, tu verras :

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Viusaliser sur streamilit : python -m streamlit run streamilit.py

---

## Accès à l’API

###  Documentation interactive
 Ouvre ton navigateur à l’adresse :  
 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Tu y trouveras :
| Endpoint | Description |
|-----------|--------------|
| `/health` | Vérifie le bon chargement du modèle |
| `/metadata` | Donne des informations sur le modèle et les features attendues |
| `/predict` | Calcule la probabilité qu’un joueur dure ≥ 5 ans |

---

##  Exemple d’utilisation du modèle

### 🔹 Endpoint : `/predict`
- **Méthode** : `POST`
- **URL** : `http://127.0.0.1:8000/predict?threshold=0.5`

### 🔹 Corps de la requête (JSON)

```json
{
  "gp": 65,
  "min": 24.3,
  "pts": 11.2,
  "fgm": 4.3,
  "fga": 9.7,
  "fg_pct": 44.5,
  "three_p_made": 1.6,
  "three_p_attempts": 4.5,
  "three_p_pct": 35.5,
  "ftm": 1.1,
  "fta": 1.3,
  "ft_pct": 82,
  "oreb": 0.8,
  "dreb": 3.1,
  "reb": 3.9,
  "ast": 2.4,
  "stl": 0.9,
  "blk": 0.3,
  "tov": 1.7
}
```

### 🔹 Réponse (exemple)

```json
{
  "prediction": 1,
  "probability": 0.73,
  "threshold": 0.5,
  "model": "nba_final_model.pkl"
}
```

> **Interprétation :**
> - `prediction = 1` → Le joueur est prédit comme **durable (≥5 ans)**  
> - `probability = 0.73` → Confiance du modèle : 73 %


---

##  Description du modèle

Le modèle final est un **RandomForestClassifier**, entraîné pour maximiser le **Recall** sur la classe “joueurs durables”.

###  Variables les plus influentes :

| Rang | Variable | Signification |
|------|-----------|---------------|
| 1 | GP | Nombre de matchs joués |
| 2 | ACTIVITY_INDEX | Activité globale (attaque + défense) |
| 3 | DEF_INDEX | Impact défensif |
| 4 | OFF_EFF_INDEX | Efficacité offensive |
| 5 | REB_PER_MIN | Intensité au rebond |
| 6 | CONSISTENCY_INDEX | Régularité et stabilité du jeu |

---

