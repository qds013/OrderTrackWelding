import logging
import telebot
from todoist_api_python.api import TodoistAPI

from ___tgtoken import token

# setting up logger
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# workaround to prevent disconnect on timeout
telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60

# creating telegram bot
bot = telebot.TeleBot(token)

# hadling 'start' command
@bot.message_handler(commands = ['start'])
def bot_send_welcome(message):
    message_text = """
    Добро пожаловать в систему отслеживания заказов!

    Для проверки статуса заказа просто отправьте его номер.
    Используйте /help для получения дополнительной информации.
    """
    bot.reply_to(message, message_text)

# handling 'help' command
@bot.message_handler(commands=['help'])
def bot_send_help(message):
    message_text = """
    Как использовать бот:
    1. Отправьте номер вашего заказа
    2. Получите актуальную информацию о статусе

    Пример номера заказа: ORDER123

    При возникновении проблем обратитесь к менеджеру.
    """
    bot.reply_to(message, message_text)

@bot.message_handler(func = lambda message: True)
def bot_check_order(message):
    order_number = message.text.strip().upper()
    logging.info(f"Получен запрос на заказ {order_number} от {message.from_user.username}")
    bot.reply_to(message, "Запрос статуса заказа " + order_number)


@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)
    print("*** Message arrived: " + message.text)

print("Telegram bot started...")
bot.polling(none_stop=True)
print("Telegram bot exited.")
