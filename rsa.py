import random
import pickle as pkl

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,.'

def eucAlg(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extEucAlg(a, b):
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b > 0:
        q = a // b
        r, x, y = a - q * b, x2 - q * x1, y2 - q * y1
        a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y
    d, x, y = a, x2, y2
    return d, x, y

def modInv(a, m):
    d, x, y = extEucAlg(a, m)
    if d == 1:
        return x % m
    else:
        return None

def quickMulti(a, k, n):
    b = 1
    if k == 0:
        return b
    A = a
    if k & 1 == 1:
        b = a
    for i in range(1, len(bin(k)[2:])):
        A = (A ** 2) % n
        if (k >> i) & 1 == 1:
            b = (A * b) % n
    return b

def testFermat(n, t):
    for i in range(1, t):
        a = random.randrange(2, n - 1)
        r = quickMulti(a, n - 1, n)
        if r != 1:
            return False
    return True

def genKey(p, q):
    n = p * q  # модуль алгоритма
    φ = (p - 1) * (q - 1)  # функция эйлера
    e = random.randrange(1, φ)  # экспонента зашифрования
    g = eucAlg(e, φ)
    while g != 1:
        e = random.randrange(1, φ)
        g = eucAlg(e, φ)
    d = modInv(e, φ)
    return (e, n), d

def strToInt(text):
    result = 0
    k = 1
    for c in text:
        result += alphabet.index(c) * k
        k *= len(alphabet)
    return result

def intToStr(number):
    result = ''
    while number > 0:
        result += alphabet[number % len(alphabet)]
        number //= len(alphabet)
    return result

def encrypt(keyPair, text):
    result = []
    while len(text) > 0:
        if len(text) < 5:
            block = text
            text = ''
        else:
            block = text[:5]
            text = text[5:]
        result.append(quickMulti(strToInt(block), keyPair[0], keyPair[1]))
    return pkl.dumps(result).hex()

def decrypt(d, c, modulo):
    code = pkl.loads(bytes.fromhex(c))
    result = ''
    for i in code:
        k = quickMulti(i, d, modulo)
        result += intToStr(k)
    return result

def main():
    role = input('Введите вашу роль (A, B): ')
    if role.upper() == 'A':
        action = input('Выберите действие (1 - генерация ключевой пары, 2 - расшифрование): ')
        p, q = input('Введите пару чисел (p, q): ').split(',')
        if action == '1':
            if testFermat(int(p), 13) is False or testFermat(int(q), 13) is False:
                print('Оба числа должны быть простыми')
                return
            keyPair, d = genKey(int(p), int(q))
            print('Ваш открытый ключ (e, n): ', keyPair)
            print('Ваш закрытый ключ d: ', d)
        if action == '2':
            d = int(input('Введите закрытый ключ: '))
            encrypted = input('Введите зашифрованное сообщение: ')
            print('Расшифрованное сообщение:', decrypt(d, encrypted, int(p) * int(q)))
    if role.upper() == 'B':
        keyPair = [int(x) for x in input('Введите открытый ключ (e, n): ').split(',')]
        message = str(input('Введите сообщение: '))
        encrypted = encrypt(keyPair, message)
        print('Зашифрованное сообщение:', encrypted)


if __name__ == '__main__':
    main()
