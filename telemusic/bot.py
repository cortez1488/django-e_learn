import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
#from telegram.ext.filters import
import bot_config
import logging
import sqlite3


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token=bot_config.BOT_TOKEN)
dispatcher = updater.dispatcher

def create(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = 'id: ' + str(update.effective_chat.id) +' '+ str(update.effective_user.first_name))
    print('id: ', update.effective_chat.id, update.effective_user.first_name, update.effective_user.last_name)

def start(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")



def main_handler():
    start_handler = CommandHandler('start', start)
    create_handler = MessageHandler(filters=Filters.update, callback=create)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(create_handler)

    updater.start_polling()

main_handler()
