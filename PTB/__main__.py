import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_API_TOKEN = "YOUR_TELEGRAM_API_TOKEN"
KUKI_API_KEY = "e302e13a35dcc9707e3b829a665b9533a0414656bac7e4ef32ec17fa55fa2311"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def chatbot_on(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    context.bot.send_message(chat_id=user_id, text="Chatbot is now on!")

    context.user_data[user_id] = True

def chatbot_off(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    context.bot.send_message(chat_id=user_id, text="Chatbot is now off.")

    context.user_data[user_id] = False
  
def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if context.user_data.get(user_id, False):
        user_message = update.message.text

        response = requests.post("https://api.kuki.ai/v1/ask", json={
            "user": user_id,
            "key": KUKI_API_KEY,
            "message": user_message
        })

        if response.status_code == 200:
            kuki_response = response.json()["response"]
            context.bot.send_message(chat_id=user_id, text=kuki_response)
        else:
            context.bot.send_message(chat_id=user_id, text="Sorry, I'm having trouble right now.")

def main() -> None:
    updater = Updater(token=TELEGRAM_API_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("chatbot", chatbot_on))
    dispatcher.add_handler(CommandHandler("chatbot_off", chatbot_off))
    dispatcher.add_handler(MessageHandler(None, handle_message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

