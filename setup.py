## -*- coding: utf-8 -*-
try:
	print('Trying to import packages..')
	import requests
	from datetime import datetime
	import telebot
	from telebot import types
	from bs4 import BeautifulSoup
except Exception as e:
	raise e

markup = types.ReplyKeyboardMarkup(True)
itembtn1 = types.KeyboardButton('Меню')
markup.add(itembtn1)

#
now = datetime.now()
r_admin = 742397386
bot_token = "5038248529:AAEXNNafZ7juxg9s1Y28N2jQ8WeZBEnFpds"
#
bot = telebot.TeleBot(bot_token, parse_mode='HTML')
# /start handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello!", reply_markup=markup)

@bot.message_handler(commands='new_kadastr')
def send_list(message):
	mtext = message.text
	if mtext == '/new_kadastr':
		bot.send_message(message.chat.id, """<b>Для додавання нового контрагенту відправте повідомлення по зразку:</b>
		<code>/new_kadastr НАЗВА_ДЛЯ_КОНТРАГЕНТА КАДАСТРОВИЙ_НОМЕР</code>\n
		<b>Наприклад:</b> <code>/new_kadastr Війтівська_гора_38094949494 6322056500:14:000:0017</code>

		*Ім'я контрагента записувати без пробілів!
		""")
	else:
		mtext = mtext[13:999] #fetch /new_kadastr
		first_word = mtext.split()[0]
		second_word = mtext.split()[1]
		ca_list = open('numbers.txt', 'r')
		a_id = 0
		for line in ca_list:
			line_id = line.split()[0]
			a_id = int(line_id)
			a_id += 1
		ca_list.close()
		number = open('numbers.txt', 'a')
		try:
			number.write(f'{a_id} {first_word} {second_word}\n')
		except Exception as e:
			number.write(f'0 {first_word} {second_word}\n')
		number.close()
		bot.reply_to(message, "Додано успішно")

@bot.message_handler(commands='new_permits')
def send_list(message):
	mtext = message.text
	if mtext == '/new_permits':
		bot.send_message(message.chat.id, """<b>Для додавання нового контрагенту відправте повідомлення по зразку:</b>
		<code>/new_kadastr НАЗВА_ДЛЯ_КОНТРАГЕНТА НОМЕР</code>\n
		<b>Наприклад:</b> <code>/new_permits АТБ_123 6322056500:14:000:0017</code>

		*Ім'я контрагента записувати без пробілів!
		""")
	else:
		mtext = mtext[13:999] #fetch /new_kadastr
		first_word = mtext.split()[0]
		second_word = mtext.split()[1]
		ca_list = open('permits.txt', 'r')
		a_id = 0
		for line in ca_list:
			line_id = line.split()[0]
			a_id = int(line_id)
			a_id += 1
		ca_list.close()
		number = open('permits.txt', 'a')
		try:
			number.write(f'{a_id} {first_word} {second_word}\n')
		except Exception as e:
			number.write(f'0 {first_word} {second_word}\n')
		number.close()
		bot.reply_to(message, "Додано успішно")

@bot.message_handler(commands='list_kadastr')
def request_list(message):
	list = open('numbers.txt', 'r')
	bot.send_message(message.chat.id, 'Контрагенти на провірку:')
	for line in list:
		ca_id = line.split()[0]
		ca_name = line.split()[1]
		ca_num = line.split()[2]
		bot.send_message(message.chat.id, f"{line}\nВидалити: /delete_{ca_id}")
	list.close()

@bot.message_handler(commands='list_permits')
def request_list(message):
	list = open('permits.txt', 'r')
	bot.send_message(message.chat.id, 'Контрагенти на провірку:')
	for line in list:
		ca_id = line.split()[0]
		ca_name = line.split()[1]
		ca_num = line.split()[2]
		bot.send_message(message.chat.id, f"{line}\nВидалити: /pdelete_{ca_id}")
	list.close()

@bot.message_handler(func=lambda m: True)
def delete_from_list(message):
	mtext = message.text
	mtext = mtext.split()[0]
	if mtext == '/delete_':
		caid = mtext.split()[1]
		print('123')
		with open('numbers.txt', 'r+') as f:
			list = f.readlines()
			f.seek(0)
			for line in list:
				print(line)
				if line.split()[0] != caid:
					f.write(line)
			f.truncate()
	elif mtext == '/pdelete_':
		caid = mtext.split()[1]
		print('123')
		with open('permits.txt', 'r+') as f:
			list = f.readlines()
			f.seek(0)
			for line in list:
				print(line)
				if line.split()[0] != caid:
					f.write(line)
			f.truncate()
	elif mtext == 'Меню':
		bot.send_message(message.chat.id, """
		/new_kadastr - 🔹 Новий пошук по кадастровому
		/start_kadastr - 🔹 Запуск парсингу по кадастровому номеру
		/list_kadastr - 🔹 Список пошуку по кадастровому

		/new_permits - 🔸 Новий пошук по дозволам
		/start_permits - 🔸 Запуск парсингу по дозволам
		/list_permits - 🔸 Список пошуку по дозволам""", reply_markup=markup) ###

	elif mtext == '/start_kadastr':
		try:
			number = open('numbers.txt', 'r')
			for line in number:
				first_word = line.split()[1]
				second_word = line.split()[2]
				url = f'https://e-construction.gov.ua/search_in_registers/search={second_word}' # url страницы
				try:
					r = requests.get(url)
					soup = BeautifulSoup(r.text, 'html.parser')
					tables = soup.find('table', {'class': 'table'}).text
					bot.send_message(message.chat.id, f"""📡 Інформація по: {first_word}\n✏️<a href="https://e-construction.gov.ua/search_in_registers/search={second_word}">{second_word}</a>
					<code>{str(tables)}</code>
					""")
				except Exception as e:
					bot.send_message(message.chat.id, f"Помилка: *Швидше за все неправильний кадастровий номер {e}")
					raise
		except Exception as e:
			bot.send_message(message.chat.id, f"Список пустий?")
			bot.send_message(message.chat.id, e)
	elif mtext == '/start_permits':
		try:
			number = open('permits.txt', 'r')
			for line in number:
				first_word = line.split()[1]
				second_word = line.split()[2]
				url = f'https://e-construction.gov.ua/permits_doc_new/search={second_word}' # url страницы
				try:
					r = requests.get(url)
					soup = BeautifulSoup(r.text, 'html.parser')
					tables = soup.find('div', {'class': 'dataset__left'}).text
					bot.send_message(message.chat.id, f"""📡 Інформація по: {first_word}\n✏️<a href="https://e-construction.gov.ua/permits_doc_new/search={second_word}">{second_word}</a>
					<code>{str(tables)}</code>
					""")
				except Exception as e:
					bot.send_message(message.chat.id, f"Помилка: *Швидше за все неправильний номер {e}")
					raise
		except Exception as e:
			bot.send_message(message.chat.id, f"Список пустий?")
			bot.send_message(message.chat.id, e)
	else:
		pass

bot.infinity_polling()
