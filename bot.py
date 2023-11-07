import parse_logic
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
# no - исключить ГК из отчета


bot = telebot.TeleBot(bot_config.token)

@bot.message_handler(commands=['start'])
def send_start_message(message):
	msg = """Добро пожаловать в Бот!\n\nАвтор - @kirillchechin"""
	print(f"/start by id {message.from_user.id}, Name {message.from_user.first_name} {message.from_user.last_name}, username {message.from_user.username}")
	bot.send_message(message.chat.id, msg)

# ИНтересующие ОКПД
@bot.message_handler(commands=["okpd"])
def okpd(message):
	# try:
	count = links.okpd_count()
	msg = f"""Собираю тендеры по отслеживаемым ОКПД ({count} шт.)"""
	bot.reply_to(message, msg)
	src = parse_logic.report_okpd()
	doc = open(file=src,mode='rb')
	bot.send_document(message.chat.id, doc)
	bot.reply_to(message, "Ссылка на поисковый запрос "+links.all_okpd())
	# except Exception as e:
	# 	print(e)
	# 	bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(e))


# НЕ итересующие ОКПД
@bot.message_handler(commands=["no"])
def no(message):

	nos = re.findall(r'[0-9]{11,19}', message.text)
	try:
		msg = f"""Помечаю заказы как не интересые ({len(nos)} шт.)"""
		bot.reply_to(message, msg)
		for i in nos:
			i = int(i)
			sucsess = links.log_tender_stale(i)
			if not sucsess:
				bot.reply_to(message, f"не удалось внести внести в неинтересные: {i}")

	except Exception as e:
		print(e)
		bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(e))



# Важные поставщики
@bot.message_handler(commands=["orgs"])
def vips(message):
	try:
		count = links.vip_count()
		msg = f"""Собираю тендеры отслеживаемых заказчиков ({count} шт.)"""
		bot.reply_to(message, msg)
		src = parse_logic.report_vip()
		doc = open(file=src,mode='rb')
		bot.send_document(message.chat.id, doc)

	except Exception as e:
		print(e)
		bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(e))

if __name__ == '__main__':
	print("Бот работает \n",os.getcwd())
	bot.infinity_polling()