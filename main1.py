import telebot
import config
from telebot import types
import random
import os
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Python")
    btn2 = types.KeyboardButton("SQL")
    btn3 = types.KeyboardButton("PHP")
    btn4 = types.KeyboardButton("Telegram")
    btn5 = types.KeyboardButton("Random")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.from_user.id, " Выберите нужный курс)", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'ИмяКотика':
        with open('Names.txt', encoding='utf-8') as file:
            lines = file.readlines()
        bot.send_message(message.from_user.id, lines[random.randint(0, len(lines)-1)])
    elif message.text == 'ФотоКотика':
        photo_dir = 'C:\\Users\\Женя\\Desktop\\Botinok\\Images'
        photo_files = os.listdir(photo_dir)
        random_photo = random.choice(photo_files)
        photo_path = os.path.join(photo_dir, random_photo)
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
bot.polling(none_stop=True)    