from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
# import qrcode

from cashvoucher import CashVoucher
from storer import Storer
from user import User



STORED_FILE = 'users.db'
# users = {}
storer = Storer(STORED_FILE)



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)
logger = logging.getLogger(__name__)




cash_voucher = CashVoucher()




def start(bot, update):
	telegram_user = update.message.from_user

	logger.info("Start for new user: %s" % telegram_user)

	if not telegram_user.id in users:
		users[telegram_user.id] = User(telegram_user.id)
		storer.store('users', users)

	bot.sendMessage(update.message.chat_id,
		'''Привет, %s!
		Я помогу тебе следить за расходами на покупки.
		Чтобы начать вести статистику, пришли мне фотографию чека.
		Чтобы посмотреть список команд, набери /help'''
		% telegram_user.first_name)

def help(bot, update):
	bot.sendMessage(update.message.chat_id,
		'TODO: сделать список команд')

def photo(bot, update):
	user = update.message.from_user
	photo_file = bot.get_file(update.message.photo[-1].file_id)
	file_path = str(user.id) + ".jpg"
	json_file.download(file_path)
	bot.sendMessage(update.message.chat_id,
		'Получил!')

def json_file(bot, update):
	user = update.message.from_user
	json_file = bot.get_file(update.message.document.file_id)
	file_path = str(user.id) + ".txt"
	json_file.download(file_path)
	cash_voucher.load(file_path)
	bot.sendMessage(update.message.chat_id,
		'Получил!')

def buy_list(bot, update):
	if cash_voucher.isEmpty() == 0:
		for buy_name in cash_voucher.parsed['items']:
			bot.sendMessage(update.message.chat_id,
				buy_name['name'])
	else:
		bot.sendMessage(update.message.chat_id,
			'Чек не просканирован!')



def main():
	global users
	users = storer.restore('users')
	if users is None:
		users = {}

	token = open('token.txt').read()

	updater = Updater(token=token)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('help', help))
	dispatcher.add_handler(MessageHandler(Filters.photo, photo))
	dispatcher.add_handler(MessageHandler(Filters.document, json_file))
	dispatcher.add_handler(CommandHandler('list', buy_list))

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()

