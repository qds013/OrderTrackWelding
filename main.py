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

    !!! Сейчас работает тестовый режим: заказ должен быть ORDER123

    При возникновении проблем обратитесь к менеджеру.
    """
    bot.reply_to(message, message_text)

#handling any input as order number
@bot.message_handler(func = lambda message: True)
def bot_check_order(message):
    order_number = message.text.strip().upper()
    logger.info(f"Получен запрос информации о заказе: {order_number} от: {message.from_user.username}")
    # bot.reply_to(message, "Запрос статуса заказа " + order_number)

    if not validate_order_number(order_number):
        logger.info(f"Некорректный номер заказа {order_number}")
        bot.reply_to(message, "🔴 Некорректный формат номера заказа.")
        return
    
    try:
        labels = ["Тестирование"]
        logger.info(f"Заказ {order_number} статус {', ' . join(labels)}")
        response = f"📦 Заказ №{order_number}\n"
        response += f"📋 Статус: {', ' . join(labels)}\n"
        bot.reply_to(message, response)    
    except Exception as e:
        logger.error(f"Ошибка при обработке заказа {order_number}: {str(e)}")
        response = f"🔴 Произошла ошибка при поиске заказа №{order_number} . Попробуйте позже.\n\n"
        bot.reply_to(message, response)

# handling any incoming text by echo message
"""
@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)
    print("*** Message arrived: " + message.text)
"""

def validate_order_number(order_number):
    return(order_number == "ORDER123")

# запуск бота
if __name__ == "__main__":
    try:
        logger.info("Telegram bot started...")
        bot.polling(non_stop=True)
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
    finally:
        logger.info("Telegram bot exited.")
