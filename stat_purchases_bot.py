from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
# import qrcode

from storer import Storer
from user import User



STORED_FILE = 'users.db'
storer = Storer(STORED_FILE)



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)
logger = logging.getLogger(__name__)


# Старт бота, регистрация пользователя
def start(bot, update):
	telegram_user = update.message.from_user

	logger.info("Start for user: %s" % telegram_user)

	if not telegram_user.id in users:
		users[telegram_user.id] = User(telegram_user.id)
		storer.store('users', users)

	bot.sendMessage(update.message.chat_id,
		'Привет, %s!\n'
		'Я помогу тебе следить за расходами на покупки.\n'
		'Чтобы начать вести статистику, пришли мне json-файл с иформацией.\n'
		'Чтобы посмотреть список команд, набери /help'
		% telegram_user.first_name)

# Список команд
def help(bot, update):
	bot.sendMessage(update.message.chat_id,
		'TODO: сделать список команд')

# Сообщение с фото
def photo(bot, update):
	user = update.message.from_user

	photo_file = bot.get_file(update.message.photo[-1].file_id)
	file_path = str(user.id) + ".jpg"
	json_file.download(file_path)

	bot.sendMessage(update.message.chat_id, 'Получил!')

# Сообщение с файлом
def json_file(bot, update):
	telegram_user = update.message.from_user

	if not telegram_user.id in users:
		bot.sendMessage(update.message.chat_id,
			'Чтобы начать вести статистику отправь /start')
		return

	json_file = bot.get_file(update.message.document.file_id)
	file_path = str(telegram_user.id) + ".txt"
	json_file.download(file_path)

	user = users[telegram_user.id]
	user.add_purchase(file_path)

	os.remove(file_path)

	bot.sendMessage(update.message.chat_id, 'Получил!')

# Итоговая сумма
def sum(bot, update):
	telegram_user = update.message.from_user

	if not telegram_user.id in users:
		bot.sendMessage(update.message.chat_id,
			'Чтобы начать вести статистику, отправь /start')
		return

	user = users[telegram_user.id]
	bot.sendMessage(update.message.chat_id,
		'Общая сумма = %s'
		% user.sum)

# Очистка статистики
def clean(bot, update):
	telegram_user = update.message.from_user

	if not telegram_user.id in users:
		bot.sendMessage(update.message.chat_id,
			'Нет данных для удаления.\n'
			'Чтобы начать вести статистику, отправь /start')
		return

	user = users[telegram_user.id]
	user.sum = 0;

	bot.sendMessage(update.message.chat_id,
		'Статистика удалена')




def main():
	global users
	users = storer.restore('users')
	if users is None:
		users = {}

	token = open('token.txt').read()

	updater = Updater(token)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('help', help))
	dispatcher.add_handler(MessageHandler(Filters.photo, photo))
	dispatcher.add_handler(MessageHandler(Filters.document, json_file))
	dispatcher.add_handler(CommandHandler('sum', sum))
	dispatcher.add_handler(CommandHandler('clean', clean))

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()

