from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
# import qrcode

from storer import Storer
from user import User
from helper_classes import myfilters
from helper_classes.date import Date

STORED_FILE = 'users.db'
storer = Storer(STORED_FILE)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Старт бота, регистрация пользователя
def start(bot, update):
    telegram_user = update.message.from_user

    logger.info("Start for user: %s" % telegram_user)

    if not (telegram_user.id in users):
        users[telegram_user.id] = User(telegram_user.id)
        storer.store('users', users)

    bot.sendMessage(update.message.chat_id,
        'Привет, %s!\n'
        'Я помогу тебе следить за расходами на покупки.\n'
        'Чтобы начать вести статистику, пришли мне json-файл с иформацией.\n'
        'Чтобы посмотреть список команд, набери /help'
        % telegram_user.first_name)


# Список команд
def commands_list(bot, update):
    bot.sendMessage(update.message.chat_id,
        'Список команд:\n'
        '"Сумма" - показать общую сумму по всем покупкам\n'
        '/clean - очистить статистику\n'
        '"Список команд" - показать команды')


# Сообщение с фото
def photo(bot, update):
    user = update.message.from_user

    photo_file = bot.get_file(update.message.photo[-1].file_id)
    file_path = str(user.id) + ".jpg"
    photo_file.download(file_path)

    bot.sendMessage(update.message.chat_id, 'Получил!')


# Сообщение с файлом
def json_file(bot, update):
    telegram_user = update.message.from_user

    if not (telegram_user.id in users):
        bot.sendMessage(update.message.chat_id, 'Чтобы начать вести статистику отправь /start')
        return

    file_json = bot.get_file(update.message.document.file_id)
    file_path = str(telegram_user.id) + ".txt"
    file_json.download(file_path)

    user = users[telegram_user.id]
    user.add_purchase(file_path)

    os.remove(file_path)

    bot.sendMessage(update.message.chat_id, 'Получил!')


# Итоговая сумма
def total_sum(bot, update):
    telegram_user = update.message.from_user

    if not (telegram_user.id in users):
        bot.sendMessage(update.message.chat_id, 'Чтобы начать вести статистику, отправь /start')
        return

    user = users[telegram_user.id]
    bot.sendMessage(update.message.chat_id, 'Общая сумма = %s' % user.get_totalsum())


# Сумма за заданный день
def get_day_sum(bot, update):
    telegram_user = update.message.from_user
    if not (telegram_user.id in users):
        bot.sendMessage(update.message.chat_id, 'Чтобы начать вести статистику, отправь /start')
        return

    date = Date(update.message.text)
    if not(date.check_date()):
        bot.sendMessage(update.message.chat_id, 'Такой даты не существует!')
        return

    user = users[telegram_user.id]
    sum = user.get_day_sum(date.get_date_key())
    if not (sum == 0):
        bot.sendMessage(update.message.chat_id, 'Сумма за день (%s) = %s' % (update.message.text, sum))
    else:
        bot.sendMessage(update.message.chat_id, 'В этот день покупок не зарегистировано.')


# Сумма за сегодня
def get_today_sum(bot, update):
    telegram_user = update.message.from_user
    if not (telegram_user.id in users):
        bot.sendMessage(update.message.chat_id, 'Чтобы начать вести статистику, отправь /start')
        return

    user = users[telegram_user.id]
    sum = user.get_today_sum()
    if not (sum == 0):
        bot.sendMessage(update.message.chat_id, 'Сумма за сегодня = %s' % sum)
    else:
        bot.sendMessage(update.message.chat_id, 'Сегодня покупок не зарегистировано.')


# Сумма за прошедшую неделю
def get_week_sum(bot, update):
    telegram_user = update.message.from_user
    if not (telegram_user.id in users):
        bot.sendMessage(update.message.chat_id, 'Чтобы начать вести статистику, отправь /start')
        return

    user = users[telegram_user.id]
    sum = user.get_week_sum()
    if not (sum == 0):
        bot.sendMessage(update.message.chat_id, 'Сумма за прошедшую неделю = %s' % sum)
    else:
        bot.sendMessage(update.message.chat_id, 'За прошедшую неделю покупок не зарегистировано.')


# Сумма за прошедший месяц
# def get_month_sum(bot, update):
#     telegram_user = update.message.from_user
#     if not (telegram_user.id in users):
#         bot.sendMessage(update.message.chat_id, 'Чтобы начать вести статистику, отправь /start')
#         return
#
#     user = users[telegram_user.id]
#     sum = user.get_month_sum()
#     if not (sum == 0):
#         bot.sendMessage(update.message.chat_id, 'Сумма за прошедший месяц = %s' % sum)
#     else:
#         bot.sendMessage(update.message.chat_id, 'За прошедший месяц покупок не зарегистировано.')
#
#
# # Сумма за прошедший год
# def get_year_sum(bot, update):
#     telegram_user = update.message.from_user
#     if not (telegram_user.id in users):
#         bot.sendMessage(update.message.chat_id, 'Чтобы начать вести статистику, отправь /start')
#         return
#
#     user = users[telegram_user.id]
#     sum = user.get_year_sum()
#     if not (sum == 0):
#         bot.sendMessage(update.message.chat_id, 'Сумма за прошедший год = %s' % sum)
#     else:
#         bot.sendMessage(update.message.chat_id, 'За прошедший год покупок не зарегистировано.')


# Очистка статистики
def clean(bot, update):
    telegram_user = update.message.from_user

    if not (telegram_user.id in users):
        bot.sendMessage(update.message.chat_id,
            'Нет данных для удаления.\n'
            'Чтобы начать вести статистику, отправь /start')
        return

    user = users[telegram_user.id]
    user.clear_archive()

    bot.sendMessage(update.message.chat_id, 'Статистика удалена')


def main():
    global users
    users = storer.restore('users')
    if users is None:
        users = {}

    token = open('token.txt').read()

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('clean', clean))

    dispatcher.add_handler(MessageHandler(Filters.photo, photo))
    dispatcher.add_handler(MessageHandler(Filters.document, json_file))

    date_filter = myfilters.DateFilter()
    today_filter = myfilters.TodayFilter()
    week_filter = myfilters.WeekFilter()
    # month_filter = myfilters.MonthFilter()
    # year_filter = myfilters.YearFilter()
    sum_filter = myfilters.SumFilter()
    help_filter = myfilters.HelpFilter()

    dispatcher.add_handler(MessageHandler(date_filter, get_day_sum))
    dispatcher.add_handler(MessageHandler(today_filter, get_today_sum))
    dispatcher.add_handler(MessageHandler(week_filter, get_week_sum))
    # dispatcher.add_handler(MessageHandler(month_filter, get_month_sum))
    # dispatcher.add_handler(MessageHandler(year_filter, get_year_sum))
    dispatcher.add_handler(MessageHandler(sum_filter, total_sum))
    dispatcher.add_handler(MessageHandler(help_filter, commands_list))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

