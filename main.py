from random import choice, randint

plfil = dict()

import telebot
bot = telebot.TeleBot('6470799266:AAH-4s5GEXY8Y3m8KtjsCZXExe1jEs5DCe8')

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Перезапуск бота"),
    telebot.types.BotCommand("/help", "Помощь"),
    telebot.types.BotCommand("/play", "Создать игру")
])


def game(ids, player, field):
    bot.send_message(ids, 'Вы играете против бота!')
    bot.send_message(ids, f'Вы играете за {player}-иков')
    botx = 'X' if player == 'O' else 'O'
    if player == 'O':
        bot_next = randint(0, 8)
        while field[bot_next] != ' ':
            bot_next = randint(0, 8)
        field[bot_next] = botx
    keyboard = telebot.types.InlineKeyboardMarkup()
    key1 = telebot.types.InlineKeyboardButton(text=field[0], callback_data='1', request_contact=True)

    key2 = telebot.types.InlineKeyboardButton(text=field[1], callback_data='2', request_contact=True)

    key3 = telebot.types.InlineKeyboardButton(text=field[2], callback_data='3', request_contact=True)
    keyboard.add(key1, key2, key3)

    key4 = telebot.types.InlineKeyboardButton(text=field[3], callback_data='4', request_contact=True)

    key5 = telebot.types.InlineKeyboardButton(text=field[4], callback_data='5', request_contact=True)

    key6 = telebot.types.InlineKeyboardButton(text=field[5], callback_data='6', request_contact=True)
    keyboard.add(key4, key5, key6)

    key7 = telebot.types.InlineKeyboardButton(text=field[6], callback_data='7', request_contact=True)

    key8 = telebot.types.InlineKeyboardButton(text=field[7], callback_data='8', request_contact=True)

    key9 = telebot.types.InlineKeyboardButton(text=field[8], callback_data='9', request_contact=True)
    keyboard.add(key7, key8, key9)
    bot.send_message(ids, f'Выберите клетку в которую хотите поставить {player}', reply_markup=keyboard)
    return player, field


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        '''Привет, я бот!
Давай сыграем в крестики-нолики!
Для этого пропишите /play''')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        '''Давай сыграем в крестики-нолики!
Для этого пропишите /play''')


@bot.message_handler(commands=['play'])
def play(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes', request_contact=True)
    keyboard.add(key_yes)
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no', request_contact=True)
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, 'Готовы?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global plfil
    if call.from_user.username not in plfil:
        plfil[call.from_user.username] = [choice(['X', 'O']), [' ' for i in range(9)]]
    fields = plfil[call.from_user.username][1]
    player = plfil[call.from_user.username][0]
    botx = 'X' if player == 'O' else 'O'
    if player != fields[0] == fields[4] == fields[8] != ' ' or\
        player != fields[2] == fields[4] == fields[6] != ' ' or\
        player != fields[0] == fields[1] == fields[2] != ' ' or\
        player != fields[3] == fields[4] == fields[5] != ' ' or\
        player != fields[6] == fields[7] == fields[8] != ' ' or\
        player != fields[0] == fields[3] == fields[6] != ' ' or\
        player != fields[1] == fields[4] == fields[7] != ' ' or\
        player != fields[2] == fields[5] == fields[8] != ' ':
        bot.send_message(call.message.chat.id, f'Победили {botx}-ики!')
        plfil[call.from_user.username] = [choice(['X', 'O']), [' ' for i in range(9)]]
    elif player == fields[0] == fields[4] == fields[8] != ' ' or\
        player == fields[2] == fields[4] == fields[6] != ' ' or\
        player == fields[0] == fields[1] == fields[2] != ' ' or\
        player == fields[3] == fields[4] == fields[5] != ' ' or\
        player == fields[6] == fields[7] == fields[8] != ' ' or\
        player == fields[0] == fields[3] == fields[6] != ' ' or\
        player == fields[1] == fields[4] == fields[7] != ' ' or\
        player == fields[2] == fields[5] == fields[8] != ' ':
        bot.send_message(call.message.chat.id, f'Победили {player}-ики!')
        plfil[call.from_user.username] = [choice(['X', 'O']), [' ' for i in range(9)]]
    elif fields.count(' ') == 0:
        bot.send_message(call.message.chat.id, 'Ничья!')
        plfil[call.from_user.username] = [choice(['X', 'O']), [' ' for i in range(9)]]
    if call.data == "yes":
        bot.send_message(call.message.chat.id, '3')
        bot.send_message(call.message.chat.id, '2')
        bot.send_message(call.message.chat.id, '1')
        bot.send_message(call.message.chat.id, 'Начали!')
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Хорошо, когда будете готовы напишите /play')
    elif call.data == "1":
        if fields[0] == ' ':
            fields[0] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "2":
        if fields[1] == ' ':
            fields[1] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "3":
        if fields[2] == ' ':
            fields[2] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "4":
        if fields[3] == ' ':
            fields[3] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "5":
        if fields[4] == ' ':
            fields[4] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "6":
        if fields[5] == ' ':
            fields[5] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "7":
        if fields[6] == ' ':
            fields[6] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "8":
        if fields[7] == ' ':
            fields[7] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    elif call.data == "9":
        if fields[8] == ' ':
            fields[8] = player
        else:
            bot.send_message(call.message.chat.id, 'Вы не можете поставить на чужую клетку!')
        if player == 'X':
            bot_next = randint(0, 8)
            while fields[bot_next] != ' ':
                bot_next = randint(0, 8)
            fields[bot_next] = 'O'
        player, fields = game(call.message.chat.id, player, fields)
    if player != fields[0] == fields[4] == fields[8] != ' ' or\
        player != fields[2] == fields[4] == fields[6] != ' ' or\
        player != fields[0] == fields[1] == fields[2] != ' ' or\
        player != fields[3] == fields[4] == fields[5] != ' ' or\
        player != fields[6] == fields[7] == fields[8] != ' ' or\
        player != fields[0] == fields[3] == fields[6] != ' ' or\
        player != fields[1] == fields[4] == fields[7] != ' ' or\
        player != fields[2] == fields[5] == fields[8] != ' ':
        bot.send_message(call.message.chat.id, f'Победили {botx}-ики!')
        plfil[call.from_user.username] = [choice(['X', 'O']), [' ' for i in range(9)]]
    elif player == fields[0] == fields[4] == fields[8] != ' ' or\
        player == fields[2] == fields[4] == fields[6] != ' ' or\
        player == fields[0] == fields[1] == fields[2] != ' ' or\
        player == fields[3] == fields[4] == fields[5] != ' ' or\
        player == fields[6] == fields[7] == fields[8] != ' ' or\
        player == fields[0] == fields[3] == fields[6] != ' ' or\
        player == fields[1] == fields[4] == fields[7] != ' ' or\
        player == fields[2] == fields[5] == fields[8] != ' ':
        bot.send_message(call.message.chat.id, f'Победили {player}-ики!')
        plfil[call.from_user.username] = [choice(['X', 'O']), [' ' for i in range(9)]]
    elif fields.count(' ') == 0:
        bot.send_message(call.message.chat.id, 'Ничья!')
        plfil[call.from_user.username] = [choice(['X', 'O']), [' ' for i in range(9)]]


bot.polling(none_stop=True, interval=0)
