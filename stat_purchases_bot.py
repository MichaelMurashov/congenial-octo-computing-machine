from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
# import qrcode
# import logging

token_file = open('token.txt')
token = token_file.read()

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
	photo_file.download(str(user.id) + '.jpg')
	update.message.reply_text('Получил!')

def json(bot, update):
	user = update.message.from_user
	json_file = bot.get_file(update.message.document.file_id)
	json_file.download(str(user.id) + '.json')
	update.message.reply_text('Получил!')




dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.photo, photo))
dispatcher.add_handler(MessageHandler(Filters.document, json))




updater.start_polling()
