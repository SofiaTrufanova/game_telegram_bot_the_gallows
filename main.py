from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import globals
import token2

sofia_trufanova_gallows_game_bot = Bot(token=token2.TOKEN)
dp = Dispatcher(sofia_trufanova_gallows_game_bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    globals.Globals.word = 'anime2'
    globals.Globals.count = 0
    globals.Globals.open_word = ['-'] * len(globals.Globals.word)
    await message.reply("Игра началась!")
    await sofia_trufanova_gallows_game_bot.send_photo(message.from_user.id,
                                                      open(globals.Globals.path_of_pictures[0], 'rb'))


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я повторю за тобой!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    if globals.Globals.count == 1:
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, "Игра не начата, нажмите на /start")
        return

    letter = msg.text
    text = ''
    if letter in globals.Globals.word:
        for i in range(len(globals.Globals.word)):
            if globals.Globals.word[i] == letter:
                globals.Globals.open_word[i] = globals.Globals.word[i]
    else:
        text = 'wrong'
        globals.Globals.wrong_moves += 1
    if globals.Globals.wrong_moves >= globals.Globals.max_moves:
        text = 'bad game'
        globals.Globals.count += 1
        globals.Globals.wrong_moves = 0
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
        await sofia_trufanova_gallows_game_bot.send_photo(msg.from_user.id,
                                                          open(globals.Globals.path_of_pictures[11], 'rb'))
        return
    if '-' not in globals.Globals.open_word:
        text = 'you won'
        globals.Globals.count += 1
        globals.Globals.wrong_moves = 0
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
        return
    text_before = ''
    for i in range(len(globals.Globals.word)):
        text_before += globals.Globals.open_word[i]
    text = text + '\n' + text_before
    await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
    await sofia_trufanova_gallows_game_bot.send_photo(msg.from_user.id,
                                                      open(globals.Globals.path_of_pictures[
                                                               globals.Globals.wrong_moves], 'rb'))


executor.start_polling(dp)
