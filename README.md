# 🥗 Rentless - Planificateur de Repas

Rentless est une application web moderne et élégante pour planifier vos repas de la semaine et générer automatiquement vos listes de courses.

## ✨ Fonctionnalités

- **Base de données de recettes** : Ajoutez, modifiez et gérez vos propres recettes.
- **Planning Hebdomadaire** : Interface intuitive pour organiser vos petits-déjeuners, déjeuners et dîners.
- **Liste de Courses Auto-générée** : Regroupe intelligemment les ingrédients de votre planning pour vous faire gagner du temps.
- **Exportation Premium** : Téléchargez votre liste de courses au format **PDF** ou **CSV**.
- **Design Glassmorphism** : Une interface moderne, fluide et responsive.

## 🚀 Installation & Lancement

### 1. Prérequis
Assurez-vous d'avoir Python 3.8+ installé.

### 2. Installation
Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/aarmad/rentless-food.git
cd rentless-food
pip install -r requirements.txt
```

### 3. Lancement
Lancez le serveur de développement :

```bash
python -m uvicorn app.main:app --reload
```

L'application sera accessible sur `http://127.0.0.1:8000`.

## 🛠️ Stack Technique

- **Backend** : FastAPI (Python)
- **Base de données** : SQLite avec SQLAlchemy ORM
- **Frontend** : HTML5 / Vanilla CSS (Glassmorphism design) / Lucide Icons
- **Templates** : Jinja2
- **PDF** : ReportLab

## 📁 Structure du Projet

- `app/main.py` : Point d'entrée et routes de l'application.
- `app/models.py` : Modèles de données SQL.
- `app/crud.py` : Logique de manipulation des données (Create, Read, Delete).
- `app/utils.py` : Algorithmes de génération de liste et exports.
- `app/static/` : Fichiers CSS et assets.
- `app/templates/` : Vues HTML.

---
Développé avec ❤️ pour simplifier votre cuisine au quotidien.
