import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Charger le Token API depuis le fichier .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Fonction pour démarrer le bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Bienvenue ! Envoie un nom de pays ou partage ta localisation pour voir les groupes Telegram."
    )

# Fonction pour chercher des groupes en fonction du texte entré
async def find_groups(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    url = f"https://api.telegramgroups.com/search?query={user_message}"  # API fictive

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            groups = "\n".join([f"{grp['name']} - {grp['link']}" for grp in data["results"]])
            await update.message.reply_text(f"Groupes trouvés :\n{groups}")
        else:
            await update.message.reply_text("Aucun groupe trouvé.")
    else:
        await update.message.reply_text("Erreur lors de la récupération des groupes.")

# Fonction pour traiter la localisation et rechercher des groupes à proximité
async def location_handler(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    lat, lon = location.latitude, location.longitude

    url = f"https://api.telegramgroups.com/search?lat={lat}&lon={lon}"  # API fictive

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            groups = "\n".join([f"{grp['name']} - {grp['link']}" for grp in data["results"]])
            await update.message.reply_text(f"Groupes trouvés à proximité :\n{groups}")
        else:
            await update.message.reply_text("Aucun groupe trouvé à proximité.")
    else:
        await update.message.reply_text("Erreur lors de la récupération des groupes.")

# Configuration du bot
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_groups))
app.add_handler(MessageHandler(filters.LOCATION, location_handler))

# Lancer le bot
if __name__ == "__main__":
    app.run_polling()