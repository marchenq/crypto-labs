import random


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
    n = p * q # модуль алгоритма
    φ = (p - 1) * (q - 1) # функция эйлера
    e = random.randrange(1, φ) # экспонента зашифрования
    g = eucAlg(e, φ)
    while g != 1:
        e = random.randrange(1, φ)
        g = eucAlg(e, φ)
    d = modInv(e, φ)
    return (e, n), d


def encrypt(keyPair, m):
    c = quickMulti(m, keyPair[0], keyPair[1])
    return c


def decrypt(d, c, modulo):
    m = quickMulti(c, d, modulo)
    return m


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
           print('Расшифрованное сообщение: ', decrypt(d, int(encrypted), int(p) * int(q)))
   if role.upper() == 'B':
       keyPair = [int(x) for x in input('Введите открытый ключ (e, n): ').split(',')]
       message = int(input('Введите сообщение: '))
       encrypted = encrypt(keyPair, message)
       print('Зашифрованное сообщение: ', encrypted)


if __name__ == '__main__':
    main()
