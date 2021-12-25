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

def insert_into_db(first_name, username, chat_id, ident_id):
    print(first_name, username, chat_id)
    con = sqlite3.connect(r"C:/Users/abhda/Desktop/djnago/e_learn/djangoenv/env/educa/db.sqlite3")
    cursor = con.cursor()
    cursor.execute("""insert into telemusic_telegramuser (first_name, username, chat_id, ident_id) values (?, ?, ?, ?)""", (first_name, username, chat_id, ident_id))
    con.commit()
    con.close()

def create(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Попытка регистрации')
    insert_into_db(first_name=update.effective_user.first_name, username=update.effective_user.username,
                   chat_id=update.effective_chat.id, ident_id=update.effective_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                                  text='Регистрация под своим же именем ' + str(update.effective_user.id))

def start(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")



def main_handler():
    start_handler = CommandHandler('start', start)
    create_handler = CommandHandler('register', callback=create)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(create_handler)

    updater.start_polling()

main_handler()
