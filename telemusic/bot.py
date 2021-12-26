import telegram
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
#from telegram.ext.filters import
import bot_config
import logging
import sqlite3


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token=bot_config.BOT_TOKEN)
dispatcher = updater.dispatcher

def get_music_to_download(update, context):
    con = sqlite3.connect(r"C:/Users/abhda/Desktop/djnago/e_learn/djangoenv/env/educa/db.sqlite3")
    cursor = con.cursor()
    cursor.execute('select name, path from telemusic_music where id = ?', (update.message.text, ))
    music = cursor.fetchall()[0]
    con.commit()
    con.close()

    context.bot.send_audio(chat_id=update.effective_chat.id, filename=music[0], audio=open(music[1], 'rb'), timeout=20)

def select_all_music_db():
    con = sqlite3.connect(r"C:/Users/abhda/Desktop/djnago/e_learn/djangoenv/env/educa/db.sqlite3")
    cursor = con.cursor()
    cursor.execute('select id, name from telemusic_music')
    massive = [music for music in cursor.fetchall()]
    con.commit()
    con.close()
    return massive

def get_music(update, context):
    massive_data = select_all_music_db()

    keys = [KeyboardButton(text = music[0]) for music in massive_data]
    reply_markup = ReplyKeyboardMarkup(keyboard=[keys], resize_keyboard=True)

    result = ''
    for music in massive_data:
        result += str(music[0]) + '. ' + str(music[1]) + '\n'

    context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=reply_markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Выберите музыку из предложенных')



def insert_into_db(first_name, username, chat_id, ident_id):
    con = sqlite3.connect(r"C:/Users/abhda/Desktop/djnago/e_learn/djangoenv/env/educa/db.sqlite3")
    cursor = con.cursor()
    cursor.execute('select * from telemusic_telegramuser where chat_id = ?', (chat_id, ))
    if not cursor.fetchall():
        cursor.execute("""insert into telemusic_telegramuser (first_name, username, chat_id, ident_id) values (?, ?, ?, ?)""", (first_name, username, chat_id, ident_id))
        flag = True
    else:
        flag = False
    con.commit()
    con.close()
    return flag

def create(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Попытка регистрации')
    flag = insert_into_db(first_name=update.effective_user.first_name, username=update.effective_user.username,
                   chat_id=update.effective_chat.id, ident_id=update.effective_user.id)

    reply_markup = ReplyKeyboardRemove(keyboard=[[KeyboardButton(text='Регистрация')]], resize_keyboard=True)

    if flag: context.bot.send_message(chat_id=update.effective_chat.id,
                                  text='Регистрация под своим же именем ' + str(update.effective_user.first_name), reply_markup=reply_markup)
    else: context.bot.send_message(chat_id=update.effective_chat.id,
                                  text='Вы уже в системе под своим же именем ' + str(update.effective_user.first_name), reply_markup=reply_markup)

def start(update: telegram.Update, context: CallbackContext):
    con = sqlite3.connect(r"C:/Users/abhda/Desktop/djnago/e_learn/djangoenv/env/educa/db.sqlite3")
    cursor = con.cursor()
    cursor.execute('select * from telemusic_telegramuser where chat_id = ?', (update.effective_chat.id,))
    if not cursor.fetchall():
        reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация'), KeyboardButton(text='Список музыки')]], resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, ты можешь зарегестрироваться", reply_markup=reply_markup)
    else:
        reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Список музыки'),]], resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуй, " + str(update.effective_user.first_name), reply_markup=reply_markup)

def message(update, context):

    if update.message.text.isdecimal():
        get_music_to_download(update, context)

    elif update.message.text == 'Регистрация':
        create(update, context)

    elif update.message.text == 'Список музыки':
        get_music(update, context)
    else: context.bot.send_message(chat_id = update.effective_chat.id, text = update.message.text)


def main_handler():
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.update, message)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)


    updater.start_polling()

main_handler()
