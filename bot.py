from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

import globals
import token2

sofia_trufanova_gallows_game_bot = Bot(token=token2.TOKEN)
dp = Dispatcher(sofia_trufanova_gallows_game_bot)


async def helpful(message):
    '''Служебная функция - для начала игры'''
    await message.reply(
        f"Игра началась! В загаданном слове {globals.Globals.Users[message.from_user.id].size_of_word} букв!")
    await sofia_trufanova_gallows_game_bot.send_photo(message.from_user.id,
                                                      open(globals.Globals.path_of_pictures[0], 'rb'))


@dp.message_handler(Text(equals="Животные"))
async def animal_choice(message: types.Message):
    '''Выбор темы про животных'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.animals)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message)


@dp.message_handler(Text(equals="Растения"))
async def plant_choice(message: types.Message):
    '''Выбор темы про растений'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.plants)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message)


@dp.message_handler(Text(equals="Физтех"))
async def mipt_choice(message: types.Message):
    '''Выбор темы про Физтех'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.mipt)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message)


@dp.message_handler(Text(equals="Общество"))
async def society_choice(message: types.Message):
    '''Выбор темы про общество'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.society)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await helpful(message)


@dp.message_handler(Text(equals="Еда"))
async def food_choice(message: types.Message):
    '''Выбор темы про еду'''
    globals.Globals.Users[message.from_user.id] = globals.Globals.User(message.from_user.id)
    globals.Globals.Users[message.from_user.id].new_word(globals.Globals.food)
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    await message.reply(
        f"Игра началась! В загаданном слове {globals.Globals.Users[message.from_user.id].size_of_word} букв!")
    await sofia_trufanova_gallows_game_bot.send_photo(message.from_user.id,
                                                      open(globals.Globals.path_of_pictures[0], 'rb'))


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    '''Обработка начала игры'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Физтех", "Растения", "Животные", "Общество", "Еда"]
    keyboard.add(*buttons)
    await message.answer("На какую тему сыграем?", reply_markup=keyboard)


def inserting_letter(letter, msg, text):
    '''Обрабатывает букву при корректном входе - проверяет, есть ли '''
    if letter in globals.Globals.Users[msg.from_user.id].word \
            or letter.upper() in globals.Globals.Users[msg.from_user.id].word:
        for i in range(globals.Globals.Users[msg.from_user.id].size_of_word):
            if globals.Globals.Users[msg.from_user.id].word[i] == letter or \
                    globals.Globals.Users[msg.from_user.id].word[i] == letter.upper():
                globals.Globals.Users[msg.from_user.id].open_word[i] = globals.Globals.Users[msg.from_user.id].word[i]
    else:
        text = 'Неверно...'
        globals.Globals.Users[msg.from_user.id].wrong_moves += 1
    return text


async def bad_game(msg):
    '''Вызывается при проигрыше'''
    text = f'Ты програл(а)... Загаданное слово: {globals.Globals.Users[msg.from_user.id].word}. \n ' \
           f'Чтобы начать новую игру, нажми /start'
    globals.Globals.Users[msg.from_user.id].count += 1
    globals.Globals.Users[msg.from_user.id].wrong_moves = 0
    await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
    await sofia_trufanova_gallows_game_bot.send_photo(msg.from_user.id,
                                                      open(globals.Globals.path_of_pictures[11], 'rb'))


async def good_game(msg):
    '''Вызывается при выигрыше'''
    text = f'Ты выиграл(а)! Загаданное слово: {globals.Globals.Users[msg.from_user.id].word}. \n ' \
           f'Чтобы начать новую игру, нажми /start'
    globals.Globals.Users[msg.from_user.id].count += 1
    globals.Globals.Users[msg.from_user.id].wrong_moves = 0
    await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)


@dp.message_handler()
async def echo_message(msg: types.Message):
    '''Получает букву и обрабатывает её - проверяет, что это действительно буква, а также то, есть ли она в слове'''
    if globals.Globals.Users[msg.from_user.id].count == 1:
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, "Игра не начата, нажмите на /start")
        return
    letter = msg.text.lower()
    text = ''
    if not letter.isalpha() or len(letter) > 1:
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, "Некорректный ввод. Попробуйте ещё раз.")
        return
    text = inserting_letter(letter, msg, text)
    if globals.Globals.Users[msg.from_user.id].wrong_moves >= 10:
        await bad_game(msg)
        return
    if '-' not in globals.Globals.Users[msg.from_user.id].open_word:
        await good_game(msg)
        return
    text_before = ''
    for i in range(globals.Globals.Users[msg.from_user.id].size_of_word):
        text_before += globals.Globals.Users[msg.from_user.id].open_word[i]
    text = text + '\n' + text_before
    await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
    await sofia_trufanova_gallows_game_bot.send_photo(msg.from_user.id,
                                                      open(globals.Globals.path_of_pictures[
                                                               globals.Globals.Users[msg.from_user.id].wrong_moves],
                                                           'rb'))
    return
