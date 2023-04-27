def game(word):
    echo_message(word)
    size = len(word)

    max_moves = 10
    wrong_moves = 0
    open_word = ['-'] * size

    while True:
        letter = input()
        if letter in word:
            for i in range(len(word)):
                if word[i] == letter:
                    open_word[i] = word[i]
        else:
            await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, 'wrong')
            wrong_moves += 1
        if wrong_moves == max_moves:
            await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, 'bad game')
            break
        if '-' not in open_word:
            print(*open_word)
            await sofia_trufanova_gallows_game_bot.send_message(msg.from_user.id, 'ypu won')
            break
        print(*open_word)
