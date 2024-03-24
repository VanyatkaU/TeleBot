import telebot

from telebot import types

import config

questions = [
    "1. Фамилия И.О. автора(ов) предложения:",
    "2. Телефон:",
    "3. Подразделение:",
    "4. Существующая ситуация:",
    "5. Проблемы/неудобства, связанные с существующей ситуацией:",
    "6. Предлагаемое решение с детальным описанием:",
    "7. Готовы ли Вы сами внедрять предложение? (Да/Нет/Требуется соисполнитель):",
    "8. Если Вы сами не готовы внедрять предложение или Вам требуется соисполнитель, то, как Вам кажется, кто может помочь в реализации предложения \n(Если соисполнитель не требуется, напишите Не требуется):"
]

# Словарь для хранения ответов пользователей
user_answers = {}

# Бот
bot = telebot.TeleBot(config.TOKEN)

# Функция для отправки сообщений админам
def send_admin_message(chat_id):
    admin_message = '\n\n'.join([f'{questions[i]}{answer}' for i, answer in enumerate(user_answers[chat_id])])
    bot.send_message(config.ADMIN_ID, f'Заявка пользователя \n{admin_message}')

# Cтарт
@bot.message_handler(commands=['start'])
def start(message):
    global username, name
    name = message.from_user.first_name
    username = message.from_user.username
    bot.reply_to(message, 'Здравствуйте! Это бот предназначен для подачи предложений по улучшениям. Чтобы подать заявку, заполните форму!')
    user_answers[message.chat.id] = []
    ask_question(message.chat.id, 0)

# Чтобы задвать вопросы пользователю
def ask_question(chat_id, question_number):
    if question_number < len(questions):
        bot.send_message(chat_id, questions[question_number])
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Подать предложение", callback_data='start'))
        bot.send_message(chat_id, 'Спасибо за предложение! \nПри необходимости отправки дополнительных файлов просьба направить их на почту gid@npptemp.com или передать в ИАС. \nСостояние Вашего предложения можно отслеживать на специальной доске,установленной на 1 этаже 5 корпуса напротив вендинговых аппаратов ! '
                                  '\nДля подачи еще одной заявки нажмите кнопку: Подать предложение', reply_markup=markup)
        user_answers[chat_id] = send_admin_message(chat_id)

@bot.callback_query_handler(func=lambda callback_data: True)
def callback_start(callback):
    if callback.data == 'start':
        start(callback.message)

# Входящие сообщения от пользователей
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_answers[message.chat.id].append(message.text)
    ask_question(message.chat.id, len(user_answers[message.chat.id]))

def start_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f'Произошла ошибка: {e}. Перезапуск бота.')

if __name__ == '__name__':
    start_bot()