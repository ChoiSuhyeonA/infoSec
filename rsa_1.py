import random
import cryptomath
import rabinMiller

def getBlockFromText(msg, BYTE_SIZE):
    totSum = 0
    i = 0
    for val in msg:
        totSum += ord(val) * BYTE_SIZE ** i
        i += 1
    return totSum


def getMultiBlockFromText(msg, BLOCK_SIZE, BYTE_SIZE):
    blockInt = []
    for blockStart in range(0, len(msg), BLOCK_SIZE):
        totSum = 0
        i = 0
        for val in msg[blockStart:blockStart+BLOCK_SIZE]:
            totSum += ord(val) * BYTE_SIZE ** i
            i += 1
        blockInt.append(totSum)
    return blockInt


def getTextFromBlock(sum, BYTE_SIZE):
    output = []
    i = 0
    while True:
        val = (sum // (BYTE_SIZE**i)) % BYTE_SIZE
        if val != 0:
            output.append(chr(val))
            i +=1
        else:
            return ''.join(output)


def getTextFromMultiBlock(sum, BLOCK_SIZE, BYTE_SIZE):
    output = []
    for subSum in sum:
        i = 0
        while True:
            val = (subSum // (BYTE_SIZE**i)) % BYTE_SIZE
            if val != 0:
                output.append(chr(val))
                i +=1
            else:
                break
    return ''.join(output)


def generateKey(keySize):
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print('Generating p prime...')
    p = rabinMiller.generateLargePrime(keySize)
    print('Generating q prime...')
    q = rabinMiller.generateLargePrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)


def encRSA(msg, publicKey):  #publicKey = (n,e)
    output = []
    n, e = publicKey
    for val in msg:
        output.append(pow(ord(val),e,n))

    return output


def encRSAwithBlock(msg, publicKey, BLOCK_SIZE, BYTE_SIZE):  #publicKey = (n,e)
    output = []
    n, e = publicKey
    for val in getMultiBlockFromText(msg, BLOCK_SIZE, BYTE_SIZE):
        output.append(pow(val,e,n))     # without ord

    return output


def decRSA(encMSG, privateKey):  #privateKey = (n,d)
    output = []
    n, d = privateKey
    for val in encMSG:
        output.append(chr(pow(val, d, n)))

    return ''.join(output)


def decRSAwithBlock(encMSG, privateKey, BLOCK_SIZE, BYTE_SIZE):  #privateKey = (n,d)
    output = []
    n, d = privateKey
    for val in encMSG:
        output.append(pow(val, d, n))   # without chr

    return getTextFromMultiBlock(output, BLOCK_SIZE, BYTE_SIZE)


def main():
    BYTE_SIZE = 256   # Static Value
    BLOCK_SIZE = 16    # Block Size
    keySize = 128  # Change it to 128
    plaintext = "Hello world! This is Python! Great Security Programming @@"

    publicKey, privateKey = generateKey(keySize)

    cipher = encRSAwithBlock(plaintext, publicKey, BLOCK_SIZE, BYTE_SIZE)
    print(cipher)
    print(decRSAwithBlock(cipher, privateKey, BLOCK_SIZE, BYTE_SIZE))


if __name__ == '__main__':
    main()