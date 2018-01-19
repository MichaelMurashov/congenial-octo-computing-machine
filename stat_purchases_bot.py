from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from CashVoucher import CashVoucher
# import qrcode
# import logging



cash_voucher = CashVoucher()




def start(bot, update):
	update.message.reply_text(
		'Привет!\n'
		'Я помогу тебе следить за расходами на покупки.\n'
		'Чтобы начать вести статистику, пришли мне фотографию чека.\n'
		'Чтобы посмотреть список команд, набери /help')

def help(bot, update):
	update.message.reply_text('TODO: сделать список команд')

def photo(bot, update):
	user = update.message.from_user
	photo_file = bot.get_file(update.message.photo[-1].file_id)
	file_path = str(user.id) + ".jpg"
	json_file.download(file_path)
	update.message.reply_text('Получил!')

def json_file(bot, update):
	user = update.message.from_user
	json_file = bot.get_file(update.message.document.file_id)
	file_path = str(user.id) + ".txt"
	json_file.download(file_path)
	cash_voucher.load(file_path)
	update.message.reply_text('Получил!')

def buy_list(bot, update):
	if cash_voucher.isEmpty() == 0:
		for buy_name in cash_voucher.parsed['items']:
			update.message.reply_text(buy_name['name'])
	else:
		update.message.reply_text('Чек не просканирован!')




token = open('token.txt').read()
updater = Updater(token=token)
dispatcher = updater.dispatcher

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# 	level=logging.INFO)





dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.photo, photo))
dispatcher.add_handler(MessageHandler(Filters.document, json_file))
dispatcher.add_handler(CommandHandler('list', buy_list))





updater.start_polling()
