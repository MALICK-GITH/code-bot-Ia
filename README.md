# 🤖 Bot de Codage Telegram

Un bot Telegram intelligent alimenté par l'IA pour vous aider avec vos tâches de codage. Utilise l'API OpenAI avec le modèle Laguna S 2.1 de Bynara.

## ✨ Fonctionnalités

- 📝 **Génération de code** - Demandez au bot d'écrire du code dans n'importe quel langage
- 🔍 **Explication de code** - Collez du code et obtenez une explication détaillée
- 🐛 **Débogage** - Décrivez vos problèmes et obtenez de l'aide pour les résoudre
- 📚 **Questions techniques** - Posez des questions sur la programmation
- 💬 **Mémoire conversationnelle** - Le bot se souvient du contexte de votre conversation
- 🌍 **Multi-langages** - Supporte plus de 20 langages de programmation

## 📋 Prérequis

- Python 3.8 ou supérieur
- Un token Telegram Bot (obtenu via [@BotFather](https://t.me/botfather))
- Une clé API OpenAI (déjà configurée dans `config.json`)

## 🚀 Installation

1. **Cloner ou télécharger ce projet**

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
   
   Les dépendances incluent :
   - `python-telegram-bot` - Pour l'API Telegram
   - `openai` - Pour l'API OpenAI
   - `python-dotenv` - Pour la gestion des variables d'environnement

3. **Configurer le token Telegram**
   
   Copiez le fichier `.env.example` vers `.env` et ajoutez votre token:
   ```bash
   copy .env.example .env
   ```
   
   Éditez le fichier `.env` et ajoutez votre token:
   ```
   TELEGRAM_TOKEN=votre_token_ici
   ```
   
   Vous pouvez également définir la variable d'environnement directement:
   
   **Windows (PowerShell):**
   ```powershell
   $env:TELEGRAM_TOKEN = "votre_token_ici"
   ```
   
   **Windows (CMD):**
   ```cmd
   set TELEGRAM_TOKEN=votre_token_ici
   ```
   
   **Linux/Mac:**
   ```bash
   export TELEGRAM_TOKEN="votre_token_ici"
   ```

4. **Vérifier la configuration**
   
   Le fichier `config.json` contient déjà la configuration de l'API OpenAI avec le modèle Laguna S 2.1.

## 🎯 Utilisation

### Démarrer le bot

```bash
python app.py
```

### Commandes disponibles

- `/start` - Message de bienvenue et introduction
- `/help` - Affiche l'aide et les commandes disponibles
- `/code [demande]` - Générer du code
- `/debug [problème]` - Aider au débogage
- `/explain [code]` - Expliquer du code
- `/lang` - Liste des langages supportés
- `/clear` - Effacer l'historique de conversation
- `/memory` - Voir l'état de la mémoire conversationnelle

### Exemples d'utilisation

**Générer du code:**
```
/code Écris une fonction pour trier un tableau en Python
/code Crée une API REST avec Express.js
/code Implémente un algorithme de recherche binaire en C++
```

**Déboguer:**
```
/debug Mon code ne fonctionne pas, voici l'erreur: [votre code et erreur]
/debug Pourquoi cette boucle ne s'arrête jamais? [votre code]
```

**Expliquer du code:**
```
/explain Explique ce que fait ce code: [votre code]
/explain Comment fonctionne cette fonction? [votre code]
```

**Questions générales:**
```
Quelle est la différence entre == et === en JavaScript?
Comment gérer les exceptions en Python?
C'est quoi une promesse en JavaScript?
```

### 💬 Mode Conversationnel avec Mémoire

Le bot conserve le contexte de votre conversation, ce qui vous permet de construire progressivement :

**Exemple de conversation progressive :**
```
Vous: Crée-moi une classe User en Python
Bot: [Génère la classe User de base]

Vous: Ajoute-lui une méthode login
Bot: [Ajoute la méthode login à la classe existante]

Vous: Ajoute aussi une méthode logout
Bot: [Ajoute la méthode logout en conservant le reste]

Vous: Maintenant ajoute des attributs pour le profil
Bot: [Ajoute les attributs profil en gardant login et logout]
```

**Gestion de la mémoire :**
- Le bot conserve les 10 derniers échanges
- Utilisez `/memory` pour voir l'état de la mémoire
- Utilisez `/clear` pour effacer l'historique et recommencer

## 📝 Langages supportés

- Python
- JavaScript
- TypeScript
- Java
- C++
- C
- C#
- Go
- Rust
- PHP
- Ruby
- Swift
- Kotlin
- SQL
- HTML
- CSS
- Bash
- JSON
- XML
- YAML
- Markdown

## 🔧 Configuration

### Modifier le modèle IA

Le fichier `config.json` contient la configuration de l'API:

```json
{
  "models": [
    {
      "title": "Laguna S 2.1 - Bynara",
      "provider": "openai",
      "model": "laguna-s-2.1",
      "apiKey": "votre_api_key",
      "apiBase": "https://router.bynara.id/v1"
    }
  ]
}
```

Vous pouvez modifier ces paramètres pour utiliser un autre modèle ou une autre API.

### Personnaliser le prompt système

Le prompt système qui définit le comportement du bot se trouve dans la fonction `process_coding_request` dans `bot.py`. Vous pouvez le modifier pour changer le style ou les capacités du bot.

## 🛠️ Structure du projet

```
bot tG/
├── app.py              # Code principal du bot
├── config.json         # Configuration de l'API OpenAI
├── requirements.txt    # Dépendances Python
├── .env.example       # Exemple de configuration environnement
├── .gitignore         # Fichiers à ignorer par git
├── vercel.json        # Configuration Vercel
├── railway.json       # Configuration Railway
├── render.yaml        # Configuration Render
└── README.md          # Documentation
```

## 🐛 Dépannage

### Erreur: "TELEGRAM_TOKEN non défini"

Assurez-vous d'avoir défini la variable d'environnement `TELEGRAM_TOKEN` avec votre token BotFather.

### Erreur de connexion à l'API

Vérifiez que:
- Votre clé API est correcte dans `config.json`
- L'URL de l'API est accessible
- Vous avez une connexion internet active

### Le bot ne répond pas

- Vérifiez que le bot est en cours d'exécution
- Assurez-vous que le bot n'est pas bloqué par Telegram
- Vérifiez les logs pour d'éventuelles erreurs

## � Déploiement

### ⚠️ Note importante sur le déploiement

Ce bot Telegram utilise le **polling** (processus continu 24/7), ce qui le rend incompatible avec les plateformes serverless comme Vercel. Voici les options recommandées :

### Options de déploiement recommandées

#### 1. Railway (Recommandé)
- **Pourquoi** : Supporte les processus continus, gratuit pour les petits projets
- **Configuration** : `railway.json` inclus
- **Déploiement** :
  ```bash
  railway login
  railway init
  railway up
  ```

#### 2. Render (Recommandé)
- **Pourquoi** : Supporte les web services, gratuit pour les petits projets
- **Configuration** : `render.yaml` inclus
- **Déploiement** : Connectez votre repo GitHub sur render.com

#### 3. Heroku
- **Pourquoi** : Plateforme éprouvée pour les bots
- **Configuration** : Créez un `Procfile` avec `worker: python app.py`

#### 4. VPS (Serveur privé)
- **Pourquoi** : Contrôle total, coût fixe
- **Exemples** : DigitalOcean, Linode, AWS EC2
- **Configuration** : Utilisez systemd ou supervisor pour gérer le processus

### Pourquoi pas Vercel ?

Vercel est conçu pour des fonctions serverless (exécution à la demande), mais ce bot Telegram nécessite :
- Un processus continu 24/7
- Une mémoire persistante pour les conversations
- Des webhooks actifs

Le fichier `vercel.json` est inclus pour des configurations futures, mais le bot ne fonctionnera pas correctement sur Vercel sans une refonte complète de l'architecture.

### Variables d'environnement pour le déploiement

Assurez-vous de configurer ces variables sur votre plateforme de déploiement :
- `TELEGRAM_TOKEN` - Votre token Telegram Bot
- `PYTHON_VERSION` - Version Python (3.8+)

## �🔒 Sécurité

- **Ne partagez jamais** votre token Telegram ou votre clé API
- **Ne committez jamais** les fichiers contenant des secrets dans un repository public
- Utilisez des variables d'environnement pour les données sensibles
- Considérez l'utilisation d'un fichier `.env` (ajouté à `.gitignore`)

## 📝 Améliorations futures

- [x] Mode conversationnel avec historique ✅
- [ ] Support de l'exécution de code sécurisée
- [ ] Support des fichiers
- [ ] Intégration avec GitHub
- [ ] Sauvegarde des snippets de code favoris
- [ ] Mode multi-utilisateurs avec authentification
- [ ] Persistance de la mémoire (sur disque)
- [ ] Support des conversations de groupe

## 📄 Licence

Ce projet est fourni tel quel pour un usage éducatif et personnel.

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou un pull request.

## 📞 Support

Pour des questions ou des problèmes, n'hésitez pas à ouvrir une issue sur le repository.

---

**Note:** Ce bot utilise le modèle Laguna S 2.1 via l'API Bynara. Assurez-vous de respecter les conditions d'utilisation de l'API.