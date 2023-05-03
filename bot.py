from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

import globals
import token2

sofia_trufanova_gallows_game_bot = Bot(token=token2.TOKEN)
dp = Dispatcher(sofia_trufanova_gallows_game_bot)


@dp.message_handler(commands=['help'])
async def bot_documentation(msg: types.Message):
    await sofia_trufanova_gallows_game_bot.send_message(msg.chat.id, globals.Globals.documentation_text)


@dp.message_handler(commands=['stop'])
async def bot_stop(msg: types.Message):
    globals.Globals.Users[msg.chat.id] = globals.Globals.User(msg.chat.id)
    await sofia_trufanova_gallows_game_bot.send_message(msg.chat.id, "Игра завершена.")


async def helpful(message, id):
    '''Служебная функция - для начала игры'''
    await message.reply(
        f"Игра началась! В загаданном слове {globals.Globals.Users[id].size_of_word} букв!")
    await sofia_trufanova_gallows_game_bot.send_photo(id,
                                                      open(globals.Globals.path_of_pictures[0], 'rb'))


@dp.message_handler(Text(equals="Животные"))
async def animal_choice(message: types.Message):
    '''Выбор темы про животных'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.animals)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message, message.from_user.id)


@dp.message_handler(Text(equals="Растения"))
async def plant_choice(message: types.Message):
    '''Выбор темы про растений'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.plants)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message, message.from_user.id)


@dp.message_handler(Text(equals="Физтех"))
async def mipt_choice(message: types.Message):
    '''Выбор темы про Физтех'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.mipt)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message, message.from_user.id)


@dp.message_handler(Text(equals="Общество"))
async def society_choice(message: types.Message):
    '''Выбор темы про общество'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.society)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message, message.from_user.id)


@dp.message_handler(Text(equals="Еда"))
async def food_choice(message: types.Message):
    '''Выбор темы про еду'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.food)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message, message.from_user.id)


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    '''Обработка начала игры'''
    if message.chat.type == types.ChatType.PRIVATE:
        '''Чат с ботом один на один'''
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ["Физтех", "Растения", "Животные", "Общество", "Еда"]
        keyboard.add(*buttons)
        await message.answer("На какую тему сыграем?", reply_markup=keyboard)
    else:
        '''Игра в чате'''
        await message.answer("Загадывайте слово:")
        globals.Globals.Users[message.chat.id] = globals.Globals.User(message.chat.id)
        globals.Globals.Users[message.chat.id].in_game = True


def inserting_letter(letter, msg, text, id):
    '''Обрабатывает букву при корректном входе - проверяет, есть ли '''
    if letter in globals.Globals.Users[id].word \
            or letter.upper() in globals.Globals.Users[id].word:
        for i in range(globals.Globals.Users[id].size_of_word):
            if globals.Globals.Users[id].word[i] == letter or \
                    globals.Globals.Users[id].word[i] == letter.upper():
                globals.Globals.Users[id].open_word[i] = globals.Globals.Users[id].word[i]
    else:
        text = 'Неверно...'
        globals.Globals.Users[id].wrong_moves += 1
    return text


async def bad_game(msg, id):
    '''Вызывается при проигрыше'''
    text = f'Ты програл(а)... Загаданное слово: {globals.Globals.Users[id].word}. \n ' \
           f'Чтобы начать новую игру, нажми /start'
    globals.Globals.Users[id].count += 1
    globals.Globals.Users[id].wrong_moves = 0
    globals.Globals.Users[id].in_game = False
    await sofia_trufanova_gallows_game_bot.send_message(id, text)
    await sofia_trufanova_gallows_game_bot.send_photo(id,
                                                      open(globals.Globals.path_of_pictures[11], 'rb'))


async def good_game(msg, id):
    '''Вызывается при выигрыше'''
    text = f'Ты выиграл(а)! Загаданное слово: {globals.Globals.Users[id].word}. \n ' \
           f'Чтобы начать новую игру, нажми /start'
    globals.Globals.Users[id].count += 1
    globals.Globals.Users[id].wrong_moves = 0
    globals.Globals.Users[id].in_game = False
    await sofia_trufanova_gallows_game_bot.send_message(id, text)


async def game(msg, id):
    '''Обрабатывает введённые буквы'''
    if globals.Globals.Users[id].count == 1:
        await sofia_trufanova_gallows_game_bot.send_message(id, "Игра не начата, нажмите на /start")
        return

    if msg.text.lower() == globals.Globals.Users[id].word.lower():
        await good_game(msg, id)
        return

    letter = msg.text.lower()

    if not letter.isalpha() or len(letter) > 1:
        await sofia_trufanova_gallows_game_bot.send_message(id, "Некорректный ввод. Попробуйте ещё раз.")
        return

    if letter in globals.Globals.Users[id].was_used:
        await sofia_trufanova_gallows_game_bot.send_message(id,
                                                            "Вы уже вводили эту букву. Попробуйте ещё раз.")
        return

    globals.Globals.Users[id].was_used.append(letter)
    globals.Globals.Users[id].was_used.sort()

    await sofia_trufanova_gallows_game_bot.send_message(id,
                                                        f"Вы уже ввели буквы: {(', ').join(globals.Globals.Users[id].was_used)}")

    text = ''
    text = inserting_letter(letter, msg, text, id)
    if globals.Globals.Users[id].wrong_moves >= globals.Globals.max_moves:
        await bad_game(msg, id)
        return
    if '-' not in globals.Globals.Users[id].open_word:
        await good_game(msg, id)
        return
    text_before = ''
    for i in range(globals.Globals.Users[id].size_of_word):
        text_before += globals.Globals.Users[id].open_word[i]
    text = text + '\n' + text_before
    await sofia_trufanova_gallows_game_bot.send_message(id, text)
    await sofia_trufanova_gallows_game_bot.send_photo(id,
                                                      open(globals.Globals.path_of_pictures[
                                                               globals.Globals.Users[id].wrong_moves],
                                                           'rb'))
    return


@dp.message_handler()
async def echo_message(msg: types.Message):
    '''Получает букву и обрабатывает её - проверяет, что это действительно буква, а также то, есть ли она в слове
    Если игра идёт в чате, то игнорирует все слова, не относящиеся к игре, и обрабатывает загаданное слово, а
    также введённые буквы'''
    if msg.chat.type == types.ChatType.PRIVATE:
        await game(msg, msg.from_user.id)
    else:
        if globals.Globals.Users[msg.chat.id].word == "" and globals.Globals.Users[msg.chat.id].in_game:
            if not msg.text.isalpha():
                await sofia_trufanova_gallows_game_bot.send_message(msg.chat.id, 'Введите одно слово на русском языке.')
                return
            globals.Globals.Users[msg.chat.id].word = msg.text
            globals.Globals.Users[msg.chat.id].size_of_word = len(globals.Globals.Users[msg.chat.id].word)
            globals.Globals.Users[msg.chat.id].open_word = ['-'] * globals.Globals.Users[msg.chat.id].size_of_word
            await helpful(msg, msg.chat.id)
            await sofia_trufanova_gallows_game_bot.delete_message(msg.chat.id, msg.message_id)
        elif globals.Globals.Users[msg.chat.id].in_game:
            await game(msg, msg.chat.id)
