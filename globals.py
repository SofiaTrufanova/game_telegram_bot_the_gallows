import random


def random_word():
    '''Выбирает случайное слово'''
    number = random.randrange(0, len(Globals.words))
    return Globals.words[number]


class Globals:
    Users = {}
    '''Все пользователи бота (содержит класс User)'''

    class User:
        '''Класс пользователя - запоминает, кто именно отправил сообщение.
        Используется для того, чтобы бот мог работать в нескольких сессия одновременно.'''

        def __init__(self, id):
            self.user_id = id
            self.word = ""
            self.wrong_moves = 0
            self.size_of_word = 0
            self.open_word = []
            self.count = 0

        def new_word(self):
            self.word = random_word()
            self.wrong_moves = 0
            self.size_of_word = len(self.word)
            self.open_word = ['-'] * self.size_of_word

    words = [
        'ajsfljsalfkj'
    ]
    '''Словарь слов для игры'''

    path_of_pictures = [
        'pictures/0.png',
        'pictures/1.png',
        'pictures/2.png',
        'pictures/3.png',
        'pictures/4.png',
        'pictures/5.png',
        'pictures/6.png',
        'pictures/7.png',
        'pictures/8.png',
        'pictures/9.png',
        'pictures/10.png',
        'pictures/11.png',
    ]
    '''Картинки для игры'''
