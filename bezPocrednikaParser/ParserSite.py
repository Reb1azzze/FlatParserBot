import requests
import time
from telebot import TeleBot
from bs4 import BeautifulSoup

TOKEN = "7069098793:AAFkyByILM9HT-HHX2RLCUrpiOEbKRzDRPM"
URL = 'https://kzn.bezposrednikov.ru/'

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "Здарова")
    successHrefs = set()
    while True:
        response = requests.get(URL)
        if response.status_code == 200:
            usedHrefs = set()

            soup = BeautifulSoup(response.text, 'html.parser')

            flats = soup.find_all('div', 'sEnLiCell')

            for flat in flats:
                if flat.text.lower().find('1-ком.') and flat.text.find('кондиционер') != -1:
                    usedHrefs.add(flat.findNext('link').get('href'))

            print(usedHrefs.__str__())
            if (usedHrefs != successHrefs):
                bot.send_message(msg.chat.id, usedHrefs.__str__())

            successHrefs = usedHrefs.copy()
            time.sleep(2)


bot.infinity_polling()
