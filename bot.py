import parse_logic
import links
import bot_config

import telebot
import os, shutil, traceback
import glob
import re
import time

# Описание команд тг бота
# okpd - ОКПД2
# orgs - отслеживаемые заказчики
# add - добавить ОКПД или заказчика
# data - выгрузить знания бота
# about - техническая инфа о боте

# no - исключить ГК из отчета # не актуальная фича


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
		count = links.okpd_count()
		msg = f"""Собираю тендеры по отслеживаемым ОКПД ({count} шт.)"""
		bot.reply_to(message, msg)
		src = parse_logic.report_okpd()
		doc = open(file=src,mode='rb')
		bot.send_document(message.chat.id, doc)
		# bot.reply_to(message, f"[s](google.com)", parse_mode="MarkdownV2")
		bot.reply_to(message, f"<a href='{links.all_okpd()}'>Ссылка на поисковый запрос</a>", parse_mode='HTML')
	except Exception as e:
		err_msg = f"{message.from_user}:{message.text}"+traceback.format_exc()
		print(err_msg)
		bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(err_msg))

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
		err_msg = f"{message.from_user}:{message.text}"+traceback.format_exc()
		print(err_msg)
		bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(err_msg))

# Важные поставщики
@bot.message_handler(commands=["orgs"])
def vips(message):
	try:
		count = links.vip_count()
		msg = f"""Собираю тендеры отслеживаемых заказчиков ({count} шт.)"""
		bot.reply_to(message, msg)
		src = parse_logic.report_orgs()
		doc = open(file=src,mode='rb')
		bot.send_document(message.chat.id, doc)
	except Exception as e:
		err_msg = f"{message.from_user}:{message.text}"+traceback.format_exc()
		print(err_msg)
		bot.reply_to(message, "Ошибка бота, перешлите сообщение @kirillchechin: \n"+str(err_msg))

# добавить теплого заказчика или интересующий ОКПД
@bot.message_handler(commands=["add"])
def add(message):
	if  "customerIdOrg=" in message.text:
		result = links.extract_add_orgs(message.text)
		msg = "Добавлены организации из ссылки:" + "\n".join(result)
		bot.reply_to(message, msg)

	if "okpd2Ids=" in message.text:
		result = links.extract_add_okpd(message.text)
		msg = "Добавлены ОКПД из ссылки:" + "\n\t".join(result)
		bot.reply_to(message, msg)

	else:
		msg = "Что бы добавить теплого заказчика или интересующий ОКПД, пришлите ссылку на реультат поиска по окпд или по заказичку."
		bot.reply_to(message, msg)

# Выдать базу данных с параметрами в чат
@bot.message_handler(commands=["show","data"])
def data(message):
	with open(file="tender_info.db",mode='rb') as doc:
		bot.send_document(message.chat.id, doc)
	msg = "В файле содержится информация о теплых заказчиках и отслеживаемых ОКПД. Так же хранится история тендеров попавших в отчеты.\n Можете открыть файл программой SQLiteStudio \n[|Как пользоваться|](https://progtips.ru/bazy-dannyx/menedzher-baz-dannyx-sqlitestudio.html)\n[|Скачивание SQLiteStudio|](https://sqlitestudio.pl/)"
	bot.reply_to(message, msg, parse_mode='Markdown',disable_web_page_preview=True)

# Техническая инфа для обеспечения незваисимой дальнейшей поддержки
@bot.message_handler(commands=["about"])
def info(message):
	with open(file="README.md",mode='r', encoding='utf-8') as file:
		msg = file.read()
		msg = msg.replace("#","🔵")
		bot.reply_to(message, msg, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == '__main__':
	links.init_database(links.db_name)
	print("Бот работает \n",os.getcwd())
	bot.infinity_polling()