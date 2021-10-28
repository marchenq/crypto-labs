# Digital Signature Standard
# Алгоритмы взяты с https://ru.wikipedia.org/wiki/Digital_Signature_Standard

from random import randrange
from hashlib import sha1

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
        a = randrange(2, n - 1)
        r = quickMulti(a, n - 1, n)
        if r != 1:
            return False
    return True

def pq_generation(L, N):
    g = N
    n = (L - 1) // g
    b = (L - 1) % g
    while True:
        # получаем q
        while True:
            SEED = randrange(1, 2 ** g)  # получаем произвольное число, состоящее из 160 бит
            # U = SHA[SEED] XOR SHA[(SEED+1) mod 2^g]:
            U = int(sha1(bytes(hex(SEED), encoding='ascii')).hexdigest(), 16) \
                ^ int(sha1(bytes(hex((SEED + 1) % (2 ** g)), encoding='ascii')).hexdigest(), 16)
            q = U | 2 ** (N - 1) | 1
            if testFermat(q, 20):  # проверяем, является ли q простым
                break
        # получаем p
        counter = 0  # counter
        offset = 2  # offset
        while counter < 4096:
            V = []
            for k in range(n + 1):
                Vk = int(sha1(bytes(hex((SEED + offset + k) % (2 ** g)), encoding='ascii')).hexdigest(), 16)
                V.append(Vk)
            W = 0
            for i in range(n-1):
                W += V[i] * 2 ** (160 * i)
            W += (V[n] % 2 ** b) * 2 ** (n * 160)
            X = W + 2 ** (L - 1)
            c = X % (2 * q)  # Шаг 9.
            p = X - (c - 1)  # Шаг 9.
            if p >= 2 ** (L - 1):
                if testFermat(p, 10):
                    return p, q
            counter = counter + 1
            offset = offset + n + 1

def g_generation(p, q):
    while True:
        e = (p - 1) // q
        h = randrange(1, p - 1)
        g = quickMulti(h, e, p)
        if g > 1:
            break
    return g

def getKeys(g, p, q):
    x = randrange(2, q)  # x < q
    y = quickMulti(g, x, p)
    return x, y

def getParameters(L, N):
    p, q = pq_generation(L, N)
    g = g_generation(p, q)
    return p, q, g

def signatureGeneration(M, p, q, g, x):
    while True:
        k = randrange(2, q)  # k < q
        r = quickMulti(g, k, p) % q  # r = (gᵏ mod p) mod q
        s = (modInv(k, q) * (int(sha1(M).hexdigest(), 16) + x * r)) % q  # s = (kᐨ¹(SHA(M) + xr)) mod q.
        return r, s

def signatureVerification(M, r, s, p, q, g, y):
    if 0 > r > q or 0 > s > q:
        return False
    w = modInv(s, q)
    u1 = (int(sha1(M).hexdigest(), 16) * w) % q
    u2 = (r * w) % q
    v = ((quickMulti(g, u1, p) * quickMulti(y, u2, p)) % p) % q
    if v == r:
        return True
    return False


if __name__ == "__main__":
    N = 160
    L = 1024

    action = input('Введите роль (1 - отправитель, 2 - получатель): ')
    if action == '1':
        M = str.encode(input('Введите сообщение: '), 'ascii')
        p, q, g = getParameters(L, N)  # открытые параметры
        x, y = getKeys(g, p, q) # закрытый и открытый ключ
        print('Открытые параметры (p, q, g, y): ', (p, q, g, y))
        r, s = signatureGeneration(M, p, q, g, x)
        print('Ваша подпись (r, s): ', (r, s))
    if action == '2':
        M = str.encode(input('Введите сообщение: '), 'ascii')
        p, q, g, y = map(int, input('Введите открытые параметры (p, q, g, y): ').split(', '))
        r, s = map(int, input('Введите подпись (r, s): ').split(', '))
        if signatureVerification(M, r, s, p, q, g, y):
            print('Подлинность сообщения подтверждена. Вы можете доверять полученному сообщению')
        else:
            print('Подплинность сообщения не подтверждена. Не доверяйте полученным данным.')
