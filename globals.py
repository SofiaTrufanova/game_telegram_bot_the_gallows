import random


def random_word(dictionary):
    '''Выбирает случайное слово из выбранной темы (словаря)'''
    number = random.randrange(0, len(dictionary))
    return dictionary[number]


class Globals:
    max_moves = 10
    '''Максимальное количество ходов'''

    documentation_text = "Это документация для этого бота. Она доступна по команде /help. \n" \
                         "Игра начинается при нажатии на кнопку /start.\n" \
                         "Если вы играете в одиночку, то после нажатия Вы должны выбрать тему игры, и после этого" \
                         "выберется случайное слово из словаря и игра начнётся. \n" \
                         "Если Вы играете в чате, то после начала игры введите загаданное слово " \
                         "(любой участник чата может это сделать)." \
                         "После этого игра начнётся - любой человек в чате может начать угадывать буквы. \n" \
                         "Предупреждение: лучше писать по одному - боту будет легче обрабатывать сообщение. \n" \
                         "Если хотите закончить игру преждевременно, то напишите команду /stop. \n" \
                         "Все слова в игре на русском языке. \n\n" \
                         "Приятной Вам игры!"
    '''Текст при команде /help'''

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
            self.was_used = []
            self.in_game = False

        def new_word(self, dictionary):
            '''Генерирует новое слово для игры'''
            self.word = random_word(dictionary)
            self.wrong_moves = 0
            self.size_of_word = len(self.word)
            self.open_word = ['-'] * self.size_of_word

    animals = [
        'Кот',
        'Собака',
        'Капибара',
        'Голубь',
        'Медведь',
        'Лиса',
        'Волк'
    ]
    '''Словарь по теме "Животные"'''

    plants = [
        'Одуванчик',
        'Роза',
        'Хризантема',
        'Черёмуха',
        'Берёза',
        'Дуб',
        'Трава',
    ]
    '''Словарь по теме "Растения"'''

    mipt = [
        'Физтех',
        'Студент',
        'Ботать',
        'Знания',
        'Питон',
        'Физика',
        'Матан',
        'Алгебра',
        'Лекция',
        'Семинар',
        'Группа'
    ]
    '''Словарь по теме "Физтех'''

    society = [
        'Кризис',
        'Любовь',
        'Депрессия',
        'Экономика',
        'Политика',
        'Религия',
        'Революция',
        'Психология',
        'Экология'
    ]
    '''Словарь по теме "Общество'''

    food = [
        'Сосиски',
        'Макароны',
        'Суп',
        'Котлеты',
        'Чай',
        'Кофе',
        'Вода',
        'Конфеты',
        'Салат',
        'Пюре',
        'Торт',
        'Пирог',
        'Десерт',
        'Конфеты',
        'Шоколад',
        'Овощи',
        'Фрукты',
        'Картошка',
        'Огурец',
        'Перец',
        'Помидор',
        'Яблоко',
        'Киви',
        'Банан',
        'Мандарин'
    ]
    '''Словарь по теме "Еда"'''

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
