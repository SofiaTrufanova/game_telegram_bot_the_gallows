import random

words = [
    'еда',
    'ботать',
    'Физтех',
    'Лабы',
    'Любовь',
    'воздух',
    'база',
    'кринж'
]


def random_word():
    number = random.randrange(1, len(words))
    return words[number]
