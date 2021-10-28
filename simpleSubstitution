def simpleReplacementCypher(key, message, action):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    result = ''
    if action == 'd':
        alphabet, key = key, alphabet
    for letter in message:
        if letter.upper() in alphabet:  # проверяем, есть ли такой символ в алфавите
            index = alphabet.index(letter.upper())
            if letter.isupper():
                result += key[index]
            else:
                result += key[index].lower()
        else:
            result += letter  # если такого символа в алфавите нет, просто дописываем его в исходном виде
    return result

def main():
    action = input('Введите e, если хотите зашифровать сообщение и d, если расшифровать: ')
    message = input('Введите сообщение на русском языке: ')
    key = input('Введите ключ из 33 неповторяющихся символов русского алфавита: ')  # ЧПСКИЯЁЮУЕФШАМЙЬЩБЫДЪЛТЦГВРЖЗХОНЭ
    if action == 'e':
        print(simpleReplacementCypher(key, message, 'e'))
    elif action == 'd':
        print(simpleReplacementCypher(key, message, 'd'))


if __name__ == '__main__':
    main()
