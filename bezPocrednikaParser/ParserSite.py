import requests
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from bs4 import BeautifulSoup


TOKEN = "7069098793:AAFQJ9187TCSxR8w79mp4w4C7LXGzuDxiqQ"
URL = 'https://kzn.bezposrednikov.ru/'

bot = TeleBot(TOKEN)
users = set()
used_hrefs_conditioner = set()
used_hrefs = set()


@bot.message_handler(commands=["start"])
def start(msg):
    users.add(msg.chat.id)
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add("/-conditioner")
    markup.add("/+conditioner")
    markup.add("/alive")
    bot.send_message(msg.chat.id, "Привет, жми Кнопку и я буду искать квартиры", reply_markup=markup)


@bot.message_handler(commands=["+conditioner"])
def send_messages(msg):
    global used_hrefs_conditioner
    success_hrefs = find_success_flats(True) - used_hrefs_conditioner
    if len(success_hrefs) != 0:
        for user in users:
            bot.send_message(user, success_hrefs.__str__())
        used_hrefs_conditioner.update(success_hrefs)
    else:
        bot.reply_to(msg, "Новых квартир пока нет")


@bot.message_handler(commands=["-conditioner"])
def send_messages(msg):
    global used_hrefs
    success_hrefs = find_success_flats(False) - used_hrefs
    if len(success_hrefs) != 0:
        for user in users:
            bot.send_message(user, success_hrefs.__str__())
        used_hrefs.update(success_hrefs)
    else:
        bot.reply_to(msg, "Новых квартир пока нет")


def find_success_flats(conditioner):
    response = requests.get(URL)
    if response.status_code == 200:
        success_hrefs = set()
        soup = BeautifulSoup(response.text, 'html.parser')
        flats = soup.find_all('div', 'sEnLiCell')
        if conditioner:
            for flat in flats:
                if flat.text.find('кондиционер') != -1:
                    success_hrefs.add(flat.findNext('link').get('href'))
        else:
            for flat in flats:
                if flat.text.lower().find('1-ком.') != -1:
                    success_hrefs.add(flat.findNext('link').get('href'))

        return success_hrefs


@bot.message_handler(commands=["alive"])
def alive_message(msg):
    bot.reply_to(msg, "Я жив")


bot.infinity_polling()
