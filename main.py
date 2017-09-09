from my_token import my_token
import asyncio
import random
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

from pathlib import Path
import os


"""
In this project I'm creating a simple bot that is usefull for shop centers.
Remember To '/setinline' and '/setinlinefeedback' to enable inline mode.
"""
data_path = "data"

def create_or_exists(chat_id, phone_number = None):
	if not os.path.isdir(data_path):
		os.mkdir(data_path)
	path = Path(data_path + "/" + str(chat_id))

	if not path.is_file() and phone_number:
		file = open(data_path + "/" + str(chat_id), 'w')
		file.write(phone_number)
		return
	if path.is_file() and not phone_number:
		if path.is_file():
			return True
	return False

def get_categories():
	file = open('Products/categories', 'r')
	categories = file.read().split('\n')

	return categories

def get_data_from_category(cat_name):
	files = os.listdir("Products/" + cat_name)
	return files

def submit_order(product, chat_id):
	print("User " + chat_id + "Ordered " + product)

commands = ['/start', '/buy', '/support', '/products', '/about']

async def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print("Chat: ", content_type, chat_type, chat_id)

	if content_type == 'contact':
		create_or_exists(chat_id, msg['contact']['phone_number'])
		markup = ReplyKeyboardRemove()
		await bot.sendMessage(chat_id, 'Now you can use the bot.', reply_markup = markup)

	if content_type != 'text': 
		return

	command = msg['text'].lower()

	if command.startswith('/cat'):
		message = ""
		for each in get_data_from_category(command[1:]):
			message += "\n" + "Prudoct /p_" + each

		await bot.sendMessage(chat_id, message)
		return

	if command.startswith("/p_"):
		markup = InlineKeyboardMarkup(inline_keyboard = [
				[InlineKeyboardButton(text = "Buy This", callback_data = 'buy_' + command[3:])]
			])
		await bot.sendMessage(chat_id, "Product " + command[3:], reply_markup = markup)
		return

	if command not in commands:
		print(msg['text'])
		await bot.sendMessage(chat_id, 'Invalid Command!')

	if command == '/about':
		message = \
"""*About Us:*
We are a shopping company and we can give u the products that you want in front of your home...
You can pay when you recive your product😍😍😍
Buying from us is as easy as pie and even a child can do it so dont worry💪💪💪
You can contact us using this Profile: [Support](tg://user?id=123456789)
"""
		await bot.sendMessage(chat_id, message, parse_mode = 'Markdown')

	elif command == '/start':
		markup = ReplyKeyboardMarkup(keyboard = [
				[KeyboardButton(text = "Share Phone!", request_contact = True),],
			])
		await bot.sendMessage(chat_id, 'Enter Your Phone: ', reply_markup = markup)

	else:
		if not create_or_exists(chat_id):
			markup = ReplyKeyboardMarkup(keyboard = [
				[KeyboardButton(text = "Share Phone!", request_contact = True),],
			])
			await bot.sendMessage(chat_id, 'You have to enter your phone first...', reply_markup = markup)
			return

		if command == '/buy':
			message = ""
			for each in get_categories():
				message += "\n" + "The Category /cat_" + each
			await bot.sendMessage(chat_id, message)

async def on_callback_query(msg):
	query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
	print('Callback query:', query_id, from_id, data)

	if data.startswith("buy_"):
		product = data[4:]
		submit_order(product, query_id)
		await bot.answerCallbackQuery(query_id, text='Order Submitted')
		await bot.sendMessage(msg['from']['id'], "Order Submitted")


bot = telepot.aio.Bot(my_token)

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, {'chat': on_chat_message,
									'callback_query': on_callback_query}).run_forever())

print('Listening...')

loop.run_forever()