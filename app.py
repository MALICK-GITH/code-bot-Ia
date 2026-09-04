import os
import json
import logging
from typing import Optional
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, ContextTypes
from openai import OpenAI

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Charger la configuration
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
model_config = config['models'][0]

# Initialiser le client OpenAI
client = OpenAI(
    api_key=model_config['apiKey'],
    base_url=model_config['apiBase']
)

# Obtenir le token Telegram depuis les variables d'environnement
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN non défini dans les variables d'environnement")
    exit(1)

# Langages de programmation supportés
LANGUAGES = {
    'python': '```python',
    'javascript': '```javascript',
    'java': '```java',
    'cpp': '```cpp',
    'c': '```c',
    'csharp': '```csharp',
    'go': '```go',
    'rust': '```rust',
    'php': '```php',
    'ruby': '```ruby',
    'swift': '```swift',
    'kotlin': '```kotlin',
    'typescript': '```typescript',
    'sql': '```sql',
    'html': '```html',
    'css': '```css',
    'bash': '```bash',
    'json': '```json',
    'xml': '```xml',
    'yaml': '```yaml',
    'markdown': '```markdown'
}

# Mémoire conversationnelle par utilisateur (user_id -> liste de messages)
conversation_history = {}
MAX_HISTORY_LENGTH = 10  # Garder seulement les 10 derniers échanges

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /start"""
    user_id = update.effective_user.id
    
    # Initialiser l'historique de conversation pour cet utilisateur
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    welcome_message = """
🤖 *Bienvenue sur le Bot de Codage Telegram !*

Je suis un assistant de codage alimenté par l'IA avec mémoire conversationnelle. Je peux vous aider avec:

📝 *Génération de code* - Demandez-moi d'écrire du code dans n'importe quel langage
🔍 *Explication de code* - Collez du code et je vous l'expliquerai
🐛 *Débogage* - Décrivez votre problème et je vous aiderai à le résoudre
📚 *Questions techniques* - Posez des questions sur la programmation
💬 *Conversation continue* - Je me souviens de notre conversation !

*Commandes disponibles:*
/start - Afficher ce message d'aide
/help - Afficher les commandes disponibles
/code - Générer du code
/debug - Aider au débogage
/explain - Expliquer du code
/lang - Liste des langages supportés
/clear - Effacer l'historique de conversation
/memory - Voir l'état de la mémoire

*Exemples:*
/code Écris une fonction pour trier un tableau en Python
/debug Mon code ne fonctionne pas, voici: [votre code]
/explain Explique ce que fait ce code: [votre code]

*Conversation:*
Vous pouvez simplement discuter avec moi ! Je me souviendrai du contexte de notre conversation.
"Crée-moi une classe User" -> puis "Ajoute-lui une méthode login" -> puis "Ajoute aussi une méthode logout"

Envoyez simplement votre message et je vous aiderai !
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /help"""
    help_message = """
📚 *Aide du Bot de Codage*

*Commandes:*
/start - Message de bienvenue
/help - Cette aide
/code [votre demande] - Générer du code
/debug [votre problème] - Aider au débogage
/explain [votre code] - Expliquer du code
/lang - Liste des langages supportés
/clear - Effacer l'historique de conversation
/memory - Voir l'état de la mémoire

*Utilisation générale:*
Vous pouvez simplement me poser des questions ou me donner des tâches de codage sans utiliser de commandes spécifiques.
Je me souviens de notre conversation, donc vous pouvez construire progressivement !

*Langages supportés:*
Python, JavaScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript, SQL, HTML, CSS, Bash, JSON, XML, YAML, Markdown

*Conseils:*
- Soyez spécifique dans vos demandes
- Incluez le langage souhaité si nécessaire
- Pour le débogage, incluez le code et les messages d'erreur
- Profitez de la mémoire conversationnelle pour construire progressivement
    """
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /lang"""
    langs_list = "\n".join([f"• {lang.capitalize()}" for lang in sorted(LANGUAGES.keys())])
    message = f"📝 *Langages de programmation supportés:*\n\n{langs_list}"
    await update.message.reply_text(message, parse_mode='Markdown')

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /clear - Efface l'historique de conversation"""
    user_id = update.effective_user.id
    
    if user_id in conversation_history:
        conversation_history[user_id] = []
        await update.message.reply_text("🗑️ *Historique de conversation effacé !*\n\nNous pouvons recommencer à zéro.", parse_mode='Markdown')
    else:
        await update.message.reply_text("ℹ️ *Aucun historique à effacer.*\n\nNotre conversation est déjà vide.", parse_mode='Markdown')

async def memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /memory - Affiche l'état de la mémoire"""
    user_id = update.effective_user.id
    
    if user_id not in conversation_history or len(conversation_history[user_id]) == 0:
        await update.message.reply_text("🧠 *Mémoire vide*\n\nAucune conversation en cours.", parse_mode='Markdown')
    else:
        history_count = len(conversation_history[user_id])
        message = f"🧠 *État de la mémoire*\n\n"
        message += f"• Messages en mémoire: {history_count}\n"
        message += f"• Capacité maximale: {MAX_HISTORY_LENGTH}\n"
        message += f"• Utilisation: {history_count}/{MAX_HISTORY_LENGTH}"
        await update.message.reply_text(message, parse_mode='Markdown')

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /code"""
    if not context.args:
        await update.message.reply_text("❌ Veuillez spécifier ce que vous voulez que je code.\nExemple: /code Écris une fonction pour trier un tableau en Python")
        return
    
    request = ' '.join(context.args)
    await process_coding_request(update, f"Génère du code pour: {request}")

async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /debug"""
    if not context.args:
        await update.message.reply_text("❌ Veuillez décrire votre problème ou fournir votre code.\nExemple: /debug Mon code ne fonctionne pas: [votre code]")
        return
    
    problem = ' '.join(context.args)
    await process_coding_request(update, f"Aide-moi à déboguer ce problème: {problem}")

async def explain_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour la commande /explain"""
    if not context.args:
        await update.message.reply_text("❌ Veuillez fournir le code à expliquer.\nExemple: /explain Explique ce code: [votre code]")
        return
    
    code = ' '.join(context.args)
    await process_coding_request(update, f"Explique ce code en détail: {code}")

async def process_coding_request(update: Update, prompt: str) -> None:
    """Traite une demande de codage avec l'API OpenAI en utilisant l'historique de conversation"""
    try:
        user_id = update.effective_user.id
        
        # Initialiser l'historique si nécessaire
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Envoyer un message indiquant que le bot travaille
        status_message = await update.message.reply_text("⏳ Je réfléchis à votre demande...")
        
        # Préparer les messages pour l'API
        system_prompt = """Tu es un assistant de codage expert et utile. Tu dois:
1. Fournir du code clair, bien commenté et fonctionnel
2. Expliquer ton code quand c'est nécessaire
3. Suggérer des améliorations quand c'est pertinent
4. Formatter le code avec les balises de markdown appropriées
5. Être concis et aller droit au but
6. Si on te demande de déboguer, identifier le problème et proposer une solution
7. Si on te demande d'expliquer, être pédagogique et clair
8. Garder le contexte de la conversation pour construire progressivement sur les demandes précédentes

Réponds toujours en français sauf si demandé autrement."""
        
        # Construire la liste des messages avec l'historique
        messages = [{"role": "system", "content": system_prompt}]
        
        # Ajouter l'historique de conversation
        for msg in conversation_history[user_id]:
            messages.append(msg)
        
        # Ajouter le nouveau message utilisateur
        messages.append({"role": "user", "content": prompt})
        
        # Appel à l'API OpenAI
        response = client.chat.completions.create(
            model=model_config['model'],
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extraire la réponse
        ai_response = response.choices[0].message.content
        
        # Mettre à jour l'historique de conversation
        conversation_history[user_id].append({"role": "user", "content": prompt})
        conversation_history[user_id].append({"role": "assistant", "content": ai_response})
        
        # Garder seulement les MAX_HISTORY_LENGTH derniers échanges
        if len(conversation_history[user_id]) > MAX_HISTORY_LENGTH * 2:  # *2 car on compte user + assistant
            conversation_history[user_id] = conversation_history[user_id][-MAX_HISTORY_LENGTH * 2:]
        
        # Supprimer le message de statut
        await status_message.delete()
        
        # Envoyer la réponse
        await update.message.reply_text(ai_response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la demande: {e}")
        await update.message.reply_text(f"❌ Une erreur s'est produite: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler pour les messages généraux"""
    user_message = update.message.text
    
    # Ignorer les commandes (elles sont déjà gérées)
    if user_message.startswith('/'):
        return
    
    await process_coding_request(update, user_message)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestionnaire d'erreurs"""
    logger.error(f"Exception {context.error} causée par {update}")

def main() -> None:
    """Point d'entrée principal du bot"""
    # Créer l'application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Enregistrer les handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CommandHandler("code", code_command))
    application.add_handler(CommandHandler("debug", debug_command))
    application.add_handler(CommandHandler("explain", explain_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("memory", memory_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Gestionnaire d'erreurs
    application.add_error_handler(error_handler)
    
    # Démarrer le bot
    logger.info("Bot démarré avec succès!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Pour Vercel, nous avons besoin d'une fonction handler de niveau supérieur
def handler(request):
    """Handler pour Vercel serverless functions"""
    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'bot_ready', 'message': 'Bot Telegram de codage - Utilisez Railway ou Render pour un déploiement complet'}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }

# Alias pour Vercel (il cherche "app", "application" ou "handler")
app = handler
application = handler

if __name__ == '__main__':
    # Lancer en mode polling pour le développement local
    main()