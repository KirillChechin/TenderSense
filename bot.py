import parser
import links
import bot_config

import telebot
import os, shutil
import glob
import re
import time

# Описание команд тг бота
# okpd - ОКПД2
# orgs - отслеживаемые заказчики


bot = telebot.TeleBot(bot_config.token)

@bot.message_handler(commands=['start'])
def send_start_message(message):
	msg = """Добро пожаловать в Бот!\n\nАвтор - @kirillchechin"""
	print(f"/start by id {message.from_user.id}, Name {message.from_user.first_name} {message.from_user.last_name}, username {message.from_user.username}")
	bot.send_message(message.chat.id, msg)

# ИНтересующие ОКПД
@bot.message_handler(commands=["okpd"])
def okpd(message):
	try:
		msg = f"""Собираю тендеры по отслеживаемым ОКПД (32 шт.)"""
		bot.reply_to(message, msg)
		src = parser.result_table(parser.report_okpd())
		doc = open(file=src,mode='rb')
		bot.send_document(message.chat.id, doc)
		bot.reply_to(message, "Ссылка на поисковый запрос "+links.all_okpd)
	except Exception as e:
		print(e)
		bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(e))


# Важные поставщики
@bot.message_handler(commands=["orgs"])
def vips(message):
	try:
		msg = f"""Собираю тендеры отслеживаемых заказчиков ({len(links.vip_orgs())} шт.)"""
		bot.reply_to(message, msg)
		src = parser.result_table(parser.report_vip())
		doc = open(file=src,mode='rb')
		bot.send_document(message.chat.id, doc)

	except Exception as e:
		print(e)
		bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(e))

if __name__ == '__main__':
	print("Бот работает \n",os.getcwd())
	bot.infinity_polling()