def affineRecurrentCypher(keyPair1, keyPair2, message, action):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    alphaKeys = {1: keyPair1[0], 2: keyPair2[0]}
    betaKeys = {1: keyPair1[1], 2: keyPair2[1]}
    i = 3
    if action == 'e':
        encrypted = ''
        for letter in message:
            alpha, beta = getKeyPair(i, alphaKeys, betaKeys)
            if letter.upper() in alphabet:
                index = alphabet.index(letter.upper())
                if letter.isupper():
                    encrypted += alphabet[(index * alpha + beta) % len(alphabet)]
                else:
                    encrypted += alphabet[(index * alpha + beta) % len(alphabet)].lower()
            else:
                encrypted += letter
            i += 1
        return encrypted
    elif action == 'd':
        decrypted = ''
        for letter in message:
            alpha, beta = getKeyPair(i, alphaKeys, betaKeys)
            modInvA = modInv(alpha, len(alphabet))
            if letter.upper() in alphabet:
                index = alphabet.index(letter.upper())
                if letter.isupper():
                    decrypted += alphabet[(index - beta) * modInvA % len(alphabet)]
                else:
                    decrypted += alphabet[(index - beta) * modInvA % len(alphabet)].lower()
            else:
                decrypted += letter
            i += 1
        return decrypted

def getKeyPair(i, alpha, beta):
    alpha[i] = (alpha[i-1] * alpha[i-2])
    beta[i] = (beta[i-1] + beta[i-2])
    return alpha[i], beta[i]

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
    keyPair1 = [int(x) for x in input("Введите ключевую пару α₁, β₁: ").split(',')]
    keyPair2 = [int(x) for x in input("Введите ключевую пару α₂, β₂: ").split(',')]
    if action == 'e':
        print(affineRecurrentCypher(keyPair1, keyPair2, message, 'e'))
    elif action == 'd':
        print(affineRecurrentCypher(keyPair1, keyPair2, message, 'd'))


if __name__ == '__main__':
    main()
