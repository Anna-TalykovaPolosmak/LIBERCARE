# 🧘‍♀️ LIBERCARE - Assistant Médical Intelligent

![LIBERCARE Banner](![image](https://github.com/user-attachments/assets/58fa54db-38af-4cc2-934a-a2fc0cbdf177))

## 💡 À propos

LIBERCARE est un assistant médical virtuel intelligent conçu pour vous aider à prendre soin de votre santé au quotidien. Cette application multilingue (français, anglais et russe) vous propose des recommandations médicamenteuses personnalisées, des remèdes naturels, et des articles de santé actualisés - le tout dans une interface élégante et intuitive.

## ✨ Fonctionnalités principales

### 🩺 Consultation médicale virtuelle
- **Analyse de symptômes** - Décrivez simplement vos symptômes et obtenez une analyse détaillée
- **Recommandations médicamenteuses** - Suggestions précises basées sur une base de données médicale complète
- **Alternatives naturelles** - Des remèdes à base de plantes et solutions naturelles pour chaque situation

### 🌐 Interface multilingue
- **Français** - Interface complète en français
- **English** - Full English interface
- **Русский** - Полный русский интерфейс

### 📚 Centre de ressources santé
- **Articles recommandés** - Contenus de santé pertinents mis à jour régulièrement
- **Recherche thématique** - Trouvez facilement des informations sur des sujets spécifiques
- **Sources fiables** - Articles sélectionnés depuis des sources médicales reconnues


## 🛠️ Architecture technique

LIBERCARE est construit autour de technologies de pointe:

- **Streamlit** - Framework frontend interactif
- **LangChain & Chroma** - Vectorisation et recherche sémantique des médicaments
- **OpenAI API** - Traitement du langage naturel et analyse des symptômes
- **Pandas** - Gestion et analyse des données médicales

### Structure du projet

```
LIBERCARE/
├── app.py                    # Application principale Streamlit
├── chatbot.py                # Moteur de dialogue médical intelligent
├── search_utils.py           # Outils de recherche d'articles de santé
├── styles.py                 # Styles CSS et interface utilisateur
├── translations.py           # Système de traduction multilingue
├── medicaments_propre.csv    # Base de données médicamenteuse
├── medical_db/               # Base de données vectorielle (générée)
└── .streamlit/               # Configuration et secrets
```

## ⚠️ Avertissement médical important

LIBERCARE est un outil d'information et ne remplace en aucun cas un avis médical professionnel. Consultez systématiquement un médecin pour tout problème de santé. Ce système est conçu comme un complément d'information uniquement.

- Ne pas utiliser en cas d'urgence médicale
- Toujours vérifier les contre-indications avec un professionnel
- Consulter un médecin si les symptômes persistent plus de 3 jours


## 🔮 Perspectives d'évolution

- Intégration d'une base de données de médicaments étendue
- Ajout d'un système de suivi de traitement personnalisé
- Développement d'une version mobile avec notifications
- Extension des langues disponibles
- Intégration de la téléconsultation avec des professionnels de santé

---

<div align="center">
    <p>Développé avec ❤️ pour votre santé</p>
    <p>© 2025 LIBERCARE</p>
</div>
