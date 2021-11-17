from math import sqrt

alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ,.?'

def extEucAlg(a, b):
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b > 0:
        q = a // b
        r, x, y = a - q*b, x2-q*x1, y2-q*y1
        a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y
    d, x = a, x2
    return d, x

def checkKey(matrix, modulo):
    determinant = getMatrixDeterminant(matrix)
    d, x = extEucAlg(determinant, modulo)
    return d == 1

def matrixMultiply(M1, M2):
    transp_M2 = transposeMatrix(M2)
    if len(transp_M2) == 1:
        return [sum(ele_M1*ele_M2 for ele_M1, ele_M2 in zip(row_M1, col_M2)) for col_M2 in transp_M2 for row_M1 in M1]
    else:
        return [[sum(ele_M1 * ele_M2 for ele_M1, ele_M2 in zip(row_M1, col_M2)) for col_M2 in transp_M2] for row_M1 in M1]

def transposeMatrix(m):
    return list(map(list, zip(*m)))

def getMatrixMinor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

def getMatrixDeterminant(m):
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * getMatrixDeterminant(getMatrixMinor(m, 0, c))
    return determinant

def getAlgebraicComplement(m):
    if len(m) == 2:
        return [[m[1][1], -1 * m[1][0]], [-1 * m[0][1], m[0][0]]]
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m, r, c)
            cofactorRow.append(((-1) ** (r + c)) * getMatrixDeterminant(minor))
        cofactors.append(cofactorRow)
    return cofactors

def getNewKey(i, keys, action):
    if action == 'e':
        keys[i] = matrixMultiply(keys[i - 1], keys[i - 2])
    if action == 'd':
        keys[i] = matrixMultiply(keys[i - 2], keys[i - 1])
    return keys[i]

def reverseMatrix(matrix, modulo):
    determinant = getMatrixDeterminant(matrix)
    algebraicComplement = getAlgebraicComplement(matrix)
    coefficient = extEucAlg(determinant, modulo)[1]
    reversedDeterminant = coefficient % modulo
    reversedMatrix = transposeMatrix([[(element * reversedDeterminant) % modulo for element in block] for block in algebraicComplement])
    return reversedMatrix

def hillRecurrentCypher(key1, key2, message, action):
    matrixSize = int(sqrt(len(key1)))

    keyIndexes1 = [alphabet.index(letter.upper()) for letter in key1]
    keyMatrix1 = [keyIndexes1[i:i + matrixSize] for i in range(0, len(keyIndexes1), matrixSize)]  # ключевая матрица1
    keyIndexes2 = [alphabet.index(letter.upper()) for letter in key2]
    keyMatrix2 = [keyIndexes2[i:i + matrixSize] for i in range(0, len(keyIndexes2), matrixSize)]  # ключевая матрица2

    if (checkKey(keyMatrix1, len(alphabet)) != 1) and (checkKey(keyMatrix2, len(alphabet)) != 1):
        return 'Оба ключа не подходят, поскольку детерминанты их матрицы не входят в группу обратимых элементов кольца.'
    elif checkKey(keyMatrix1, len(alphabet)) != 1:
        return 'Первый ключ не подходит, поскольку детерминант его матрицы не входит в группу обратимых элементов кольца.'
    elif checkKey(keyMatrix2, len(alphabet)) != 1:
        return 'Второй ключ не подходит, поскольку детерминант его матрицы не входит в группу обратимых элементов кольца.'

    keys = {1: keyMatrix1, 2: keyMatrix2}

    messageIndexes = [alphabet.index(letter.upper()) for letter in message]
    messageVectors = [[messageIndexes[i:i + matrixSize]] for i in range(0, len(messageIndexes), matrixSize)]

    i = 3

    if action == 'e':
        encrypted = ''
        encryptedBlocks = []
        for vector in messageVectors:
            keyMatrix = getNewKey(i, keys, 'e')
            encryptedBlocks.append(matrixMultiply(keyMatrix, transposeMatrix(vector)))
            i += 1
        for block in encryptedBlocks:
            for element in block:
                encrypted += alphabet[element % len(alphabet)]
        return encrypted
    elif action == 'd':
        decrypted = ''
        decryptedBlocks = []
        reversedKeys = {1: reverseMatrix(keyMatrix1, len(alphabet)), 2: reverseMatrix(keyMatrix2, len(alphabet))}
        for vector in messageVectors:
            keyMatrix = getNewKey(i, reversedKeys, 'd')
            decryptedBlocks.append(matrixMultiply(keyMatrix, transposeMatrix(vector)))
            i += 1
        for block in decryptedBlocks:
            for element in block:
                decrypted += alphabet[element % len(alphabet)]
        return ' '.join(decrypted.split())


def main():
    action = input('Введите e, если хотите зашифровать сообщение и d, если расшифровать: ')
    key1 = input('Введите первый ключ, длина которого равна квадрату целого числа (4, 9, 16, ...): ')
    key2 = input('Введите второй ключ, длина которого равна квадрату целого числа (4, 9, 16, ...): ')
    message = input('Введите сообщение на русском языке: ')
    if (int(sqrt(len(key1)) + 0.5) ** 2 == len(key1)) and (int(sqrt(len(key2)) + 0.5) ** 2 == len(key2)):  # проверка, что ключ является квадратом
        while len(message) % int(sqrt(len(key1))) != 0:  # дописываем пробелы, если длина не кратна корню размера ключа
            message += ' '
        if action == 'e':
            print(hillRecurrentCypher(key1, key2, message, 'e'))
        elif action == 'd':
            print(hillRecurrentCypher(key1, key2, message, 'd'))
    else:
        print('Неправильный ключ. Убедитесь, что его длина является квадратом целого числа.')


if __name__ == '__main__':
    main()
