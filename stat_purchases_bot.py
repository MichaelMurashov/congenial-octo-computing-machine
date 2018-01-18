from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
# import qrcode
# import logging

token = open('token.txt').read()
updater = Updater(token=token)
dispatcher = updater.dispatcher

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# 	level=logging.INFO)




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
	update.message.reply_text('Получил!')

	file = open(file_path, encoding='utf-8')
	parsed_str = json.load(file)
	update.message.reply_text(str(parsed_str["ecashTotalSum"]))





dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.photo, photo))
dispatcher.add_handler(MessageHandler(Filters.document, json_file))




updater.start_polling()
