import telebot
from telebot import types
import sqlite3
from config import TOKEN
bot = telebot.TeleBot(TOKEN)

def get_db_connection():
    conn = sqlite3.connect('furniture_bot.db')
    conn.row_factory = sqlite3.Row
    return conn

# Стартове меню
@bot.message_handler(commands=['start'])
def start(message):
    conn = get_db_connection()
    conn.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)',
                 (message.from_user.id, message.from_user.username))
    conn.commit()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Замовити меблі', 'Консультація', 'Мої замовлення')
    bot.send_message(message.chat.id, 'Вітаємо в онлайн-магазині меблів! Оберіть опцію:', reply_markup=markup)

# Обробка головного меню
@bot.message_handler(func=lambda message: True)
def main_menu(message):
    if message.text == 'Замовити меблі':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Ліжко', 'Стіл', 'Крісло', 'Назад')
        bot.send_message(message.chat.id, 'Оберіть товар:', reply_markup=markup)

    elif message.text == 'Консультація':
        bot.send_message(message.chat.id, 'Зателефонуйте нам: +380991112233 або напишіть у чат.')

    elif message.text == 'Мої замовлення':
        conn = get_db_connection()
        orders = conn.execute('SELECT product, date FROM orders WHERE user_id=?', (message.from_user.id,)).fetchall()
        conn.close()
        if orders:
            response = '\n'.join([f"{order['product']} від {order['date']}" for order in orders])
        else:
            response = 'Ви ще нічого не замовляли.'
        bot.send_message(message.chat.id, response)

    elif message.text in ['Ліжко', 'Стіл', 'Крісло']:
        conn = get_db_connection()
        conn.execute('INSERT INTO orders (user_id, product) VALUES (?, ?)', (message.from_user.id, message.text))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, f'Ви замовили {message.text}. З вами зв’яжуться!')

    elif message.text == 'Назад':
        start(message)

bot.polling()
