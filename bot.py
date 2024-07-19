import telebot
import time
from parser_tachek import Parser

BOT_TOKEN = '7361801823:AAHIeQ6VRzKsSmlPuSoQdUo4wlu8mmZjIhY'
YOUR_CHAT_ID = '742516885'
DRUG_CHAT_ID = '1010982531'

bot = telebot.TeleBot(BOT_TOKEN)
parser = Parser()

if __name__ == '__main__':
    while True:

        
        res = parser.parse()
        if res:
            for i in res:
                bot.send_message(YOUR_CHAT_ID, i)
                bot.send_message(DRUG_CHAT_ID, i)
        
        time.sleep(900)