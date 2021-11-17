def affineCypher(keyPair, message, action):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    alpha, beta = keyPair[0], keyPair[1]
    if action == 'e':
        encrypted = ''
        for letter in message:
            if letter.upper() in alphabet:
                index = alphabet.index(letter.upper())
                if letter.isupper():
                    encrypted += alphabet[(index * alpha + beta) % len(alphabet)]
                else:
                    encrypted += alphabet[(index * alpha + beta) % len(alphabet)].lower()
            else:
                encrypted += letter
        return encrypted
    elif action == 'd':
        decrypted = ''
        modInvA = modInv(alpha, len(alphabet))
        for letter in message:
            if letter.upper() in alphabet:
                index = alphabet.index(letter.upper())
                if letter.isupper():
                    decrypted += alphabet[(index - beta) * modInvA % len(alphabet)]
                else:
                    decrypted += alphabet[(index - beta) * modInvA % len(alphabet)].lower()
            else:
                decrypted += letter
        return decrypted

def extEucAlg(a, b):
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b > 0:
        q = a // b
        r, x, y = a - q*b, x2-q*x1, y2-q*y1
        a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y
    d, x, y = a, x2, y2
    return d, x, y

def modInv(a, m):
    d, x, y = extEucAlg(a, m)
    if d == 1:
        return x % m
    else:
        return None

def main():
    action = input('Введите e, если хотите зашифровать сообщение и d, если расшифровать: ')
    message = input('Введите сообщение на русском языке: ')
    keyPair = [int(x) for x in input("Введите ключевую пару α, β: ").split(',')]
    if action == 'e':
        print(affineCypher(keyPair, message, 'e'))
    elif action == 'd':
        print(affineCypher(keyPair, message, 'd'))


if __name__ == '__main__':
    main()
