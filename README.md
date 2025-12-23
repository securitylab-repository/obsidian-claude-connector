# 🤖 Obsidian-Claude Connector

Connectez votre vault Obsidian à l'API Claude d'Anthropic pour une expérience d'IA puissante avec vos notes !

## ✨ Fonctionnalités

- 🔍 **Recherche intelligente** - Posez des questions, Claude trouve les réponses dans vos notes
- 💬 **Chat contextuel** - Discutez avec Claude qui connaît toutes vos notes
- 📊 **Analyse de vault** - Obten

ez des insights sur votre système de notes
- ✍️ **Génération de notes** - Créez du contenu automatiquement
- 💾 **Sauvegarde directe** - Les notes générées vont directement dans Obsidian

## 📋 Prérequis

1. **Python 3.8+** installé sur votre ordinateur
2. **Clé API Anthropic** (voir instructions ci-dessous)
3. **Vault Obsidian** existant

## 🚀 Installation rapide

```bash
# Cloner le repository
git clone https://github.com/securitylab-repository/obsidian-claude-connector.git
cd obsidian-claude-connector

# Installer les dépendances
pip install -r requirements.txt

# Configurer
cp config.example.json config.json
# Éditez config.json avec votre clé API et le chemin vers votre vault

# Lancer
python obsidian_claude.py
```

## 📚 Documentation complète

- 📖 [README complet](README.md) - Guide détaillé d'installation et d'utilisation
- 🚀 [Guide de démarrage rapide](DEMARRAGE_RAPIDE.md) - Commencez en 5 minutes
- 🧪 [Test d'installation](test_installation.py) - Vérifiez que tout fonctionne

## 💰 Coûts estimés

Avec **Claude Sonnet 4.5** :
- Recherche simple : ~0.01$ par requête
- Chat conversationnel : ~0.02-0.05$ par échange

**Budget recommandé pour débuter** : 5-10$ (200-500 interactions)

## 🎯 Commandes principales

```bash
search <question>     # Rechercher dans vos notes
chat <message>        # Discuter avec Claude
analyze               # Analyser votre vault
generate <sujet>      # Générer une nouvelle note
quit                  # Quitter
```

## ⚠️ Important

- Ne partagez JAMAIS votre clé API
- Vos données restent privées (API Anthropic)
- Surveillez votre consommation sur console.anthropic.com

## 📜 Licence

Libre d'utilisation pour vos projets personnels !

---

**Créé avec ❤️ pour connecter Obsidian et Claude**
