import cryptomath
import rabinMiller
import random

def gcd(a, b):
    a, b = max(a, b), min(a, b)
    c = 1
    while c:
        c = a % b
        a = b
        b = c
    return a

def tot_list(n):
    phi = []
    x = 1
    while x < n:
        if gcd(x, n) == 1:
            phi += [x]
        x += 1
    return phi

def tot_phi(n):
    return len(tot_list(n))

p = 47
q = 59
n = p*q  #public key

e = 157        # 1< e < phi(n), gcd(e, phi(q))=1 public key
d = pow(e, tot_phi(tot_phi(n))-1, tot_phi(n))
print("d:",d)
d = pow(e, tot_phi((p-1)*(q-1))-1, (p-1)*(q-1))
print("d:",d)
d = cryptomath.findModInverse(e, tot_phi(n))
print("d:",d)

plaintext = 20
encrypt = pow(plaintext, e, n)
print("encrypted msg:", encrypt)

decrypt = pow(encrypt, d, n)
print("decrypted msg:", decrypt)

### encrypt with plaintext...

DEFAULT_BLOCK_SIZE = 1  # message length (bytes)
BYTE_SIZE = 256  # One byte has 256 different values.


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts a string message to a list of block integers. Each integer
    # represents blockSize (or whatever blockSize is set to) string characters.
    messageBytes = message.encode('ascii') # convert the string to bytes

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        # Calculate the block integer for this block of text
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize-1, -1, -1):
            asciiNumber = blockInt // (BYTE_SIZE ** i)
            blockInt = blockInt % (BYTE_SIZE ** i)
            blockMessage.insert(0,chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptRSA(msg, publicKey):
    cipherBlock = []
    n, e = publicKey
    for val in getBlocksFromText(msg):
        cipherBlock.append(pow(val, e, n))
    return cipherBlock


def decryptRSA(cipherList, msgLength, privateKey):
    decryptedBlock = []
    n, d = privateKey
    for val in cipherList:
        decryptedBlock.append(pow(val, d, n))
    return getTextFromBlocks(decryptedBlock, msgLength)


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def generateKey(keySize):
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


def main():

    msg = "Hanshin University"
    #in case of DEFAULT_BLOCK_SIZE = 1, n value should be greater than 256

    keySize = 16
    publickey, privateKey = generateKey(keySize)

    cipherList = encryptRSA(msg, publickey)
    print(cipherList)
    print(decryptRSA(cipherList, len(msg), privateKey))

if __name__ == '__main__':
    main()