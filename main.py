from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import globals
import token2
import words

sofia_trufanova_gallows_game_bot = Bot(token=token2.TOKEN)
dp = Dispatcher(sofia_trufanova_gallows_game_bot)

Users = {}


class User:
    def __init__(self, id):
        self.user_id = id
        self.word = ""
        self.wrong_moves = 0
        self.size_of_word = 0
        self.open_word = []
        self.count = 0

    def new_word(self):
        self.word = words.random_word()
        self.wrong_moves = 0
        self.size_of_word = len(self.word)
        self.open_word = ['-'] * self.size_of_word


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    Users[message.from_user.id] = User(message.from_user.id)
    Users[message.from_user.id].new_word()
    await message.reply(f"Игра началась! В загаданном слове {Users[message.from_user.id].size_of_word} букв!")
    await sofia_trufanova_gallows_game_bot.send_photo(message.from_user.id,
                                                      open(globals.Globals.path_of_pictures[0], 'rb'))


@dp.message_handler()
async def echo_message(msg: types.Message):
    if Users[msg.from_user.id].count == 1:
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, "Игра не начата, нажмите на /start")
        return
    letter = msg.text.lower()
    text = ''
    if not letter.isalpha() or len(letter) > 1:
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, "Некорректный ввод. Попробуйте ещё раз.")
        return
    if letter in Users[msg.from_user.id].word or letter.upper() in Users[msg.from_user.id].word:
        for i in range(Users[msg.from_user.id].size_of_word):
            if Users[msg.from_user.id].word[i] == letter or Users[msg.from_user.id].word[i] == letter.upper():
                Users[msg.from_user.id].open_word[i] = Users[msg.from_user.id].word[i]
    else:
        text = 'Неверно...'
        Users[msg.from_user.id].wrong_moves += 1
    if Users[msg.from_user.id].wrong_moves >= 10:
        text = f'Ты програл(а)... Загаданное слово: {Users[msg.from_user.id].word}. \n Чтобы начать новую игру, нажми /start'
        Users[msg.from_user.id].count += 1
        Users[msg.from_user.id].wrong_moves = 0
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
        await sofia_trufanova_gallows_game_bot.send_photo(msg.from_user.id,
                                                          open(globals.Globals.path_of_pictures[11], 'rb'))
        return
    if '-' not in Users[msg.from_user.id].open_word:
        text = f'Ты выиграл(а)! Загаданное слово: {Users[msg.from_user.id].word}. \n Чтобы начать новую игру, нажми /start'
        Users[msg.from_user.id].count += 1
        Users[msg.from_user.id].wrong_moves = 0
        await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
        return
    text_before = ''
    for i in range(Users[msg.from_user.id].size_of_word):
        text_before += Users[msg.from_user.id].open_word[i]
    text = text + '\n' + text_before
    await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, text)
    await sofia_trufanova_gallows_game_bot.send_photo(msg.from_user.id,
                                                      open(globals.Globals.path_of_pictures[
                                                               Users[msg.from_user.id].wrong_moves], 'rb'))
    return


executor.start_polling(dp)
