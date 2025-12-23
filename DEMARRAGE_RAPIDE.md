# 🚀 Guide de Démarrage Rapide

## Installation en 5 minutes

### 1️⃣ Installer Python
- **Windows** : https://www.python.org/downloads/ (cochez "Add to PATH")
- **Mac** : `brew install python3`
- **Linux** : `sudo apt install python3 python3-pip`

### 2️⃣ Obtenir votre clé API
1. Allez sur https://console.anthropic.com
2. Créez un compte
3. Menu "API Keys" → "Create Key"
4. **COPIEZ LA CLÉ** (important !)
5. Ajoutez 5-10$ de crédits

### 3️⃣ Configurer le script

**Ouvrez un terminal dans le dossier du script :**

```bash
# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier de configuration
cp config.example.json config.json
```

**Éditez `config.json` :**

```json
{
  "api_key": "sk-ant-api03-VOTRE_VRAIE_CLE_ICI",
  "vault_path": "C:/Users/VotreNom/Documents/VotreVault"
}
```

⚠️ **Sur Windows** : Utilisez `/` ou `\\\\` dans le chemin  
⚠️ **Le chemin doit pointer vers le DOSSIER PRINCIPAL** de votre vault

### 4️⃣ Tester l'installation

```bash
python test_installation.py
```

Si tous les tests passent ✅, vous êtes prêt !

### 5️⃣ Lancer le script

```bash
python obsidian_claude.py
```

## 🎯 Premières commandes à essayer

```bash
# Rechercher dans vos notes
search comment être plus productif

# Discuter avec Claude
chat résume mes notes de la semaine

# Analyser votre vault
analyze

# Générer une nouvelle note
generate Plan d'action 2025

# Quitter
quit
```

## 💰 Budget recommandé

- **5$** = ~200-300 recherches
- **10$** = ~500-600 recherches + analyses

Une recherche simple coûte environ **0.01-0.02$**

## 🆘 Problèmes fréquents

| Problème | Solution |
|----------|----------|
| "Module anthropic not found" | `pip install anthropic` |
| "API key invalid" | Vérifiez votre clé dans config.json |
| "Vault path not found" | Vérifiez le chemin complet |
| "No credits" | Ajoutez des crédits sur console.anthropic.com |

## 📚 Exemples d'utilisation avancés

### Recherche intelligente
```bash
search trouve toutes mes idées de projets
search quels sont mes objectifs pour cette année
search résume mes notes sur Python
```

### Organisation
```bash
chat comment organiser mes notes par thème
chat quelles notes devrais-je créer
chat suggère des connexions entre mes notes
```

### Création de contenu
```bash
generate Article sur l'IA basé sur mes notes
generate Résumé hebdomadaire de mon apprentissage
generate Plan de développement personnel
```

## 🎨 Personnalisation rapide

**Changer le modèle** (dans `obsidian_claude.py`) :

```python
# Ligne ~50-70, remplacer:
model="claude-sonnet-4-20250514"  # Intelligent mais coûteux

# Par:
model="claude-haiku-4-20250514"   # Rapide et économique
```

**Charger plus de notes** :

```python
# Ligne où vous voyez load_notes()
notes = self.load_notes(limit=20)  # Augmenter de 10 à 20
```

## ✨ Astuces

1. **Commencez petit** : Testez avec quelques recherches
2. **Surveillez les coûts** : console.anthropic.com → Usage
3. **Sauvegardez vos notes** : Le script ne modifie rien automatiquement
4. **Explorez** : Posez des questions créatives !

## 🔗 Ressources

- Documentation Anthropic : https://docs.anthropic.com
- Console API : https://console.anthropic.com
- Obsidian : https://obsidian.md

---

**Prêt à commencer ? Lancez `python obsidian_claude.py` ! 🎉**
