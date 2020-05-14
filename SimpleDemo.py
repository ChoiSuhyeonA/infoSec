import string
LETTER = string.ascii_uppercase
print(LETTER)

def CaesarEnc(message, key):
    cipher = ''
    for x in message:
        cipher += LETTER[(LETTER.find(x) + key) % len(LETTER)]
    return cipher

def CaesarDec(cipher, key):
    plaintext = ''
    for x in cipher:
        plaintext += LETTER[(LETTER.find(x) - key) % len(LETTER)]
    return plaintext

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def gcd(a, b):
    # Return the GCD of a and b using Euclid's Algorithm
    while a != 0:
        a, b = b % a, a
    return b

def eularPhi(n):
    phi = []
    x = 1
    while x < n:
        if gcd(x, n) == 1:
            phi += [x]    # phi.append(x)
        x += 1
    #print(phi)
    return len(phi)


def modinv_2ndVer(a, m):
    if gcd(a, m) != 1:
        return None
    else:
        return pow(a, eularPhi(m)-1, m)

def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

#### Caesar Encryption/Decryption ####
message = 'ABCDXYZ'
key = 7
print("message:", message, "\nkey:", key)

cipherText = CaesarEnc(message, key)
print(cipherText)
plainText = CaesarDec(cipherText, key)
print(plainText)

print(eularPhi(35))
print(modinv(5, 26))
print(findModInverse(5, 26))
print(modinv_2ndVer(5, 26))

#### affine Encryption/Decryption ####
# input : msg, k1, k2
# output : cipher

msg = 'ABCD'
k1 = 5
k2 = 7

def affineEncrypt(msg, k1, k2):
    cipher = ''
    for x in msg:
        cipher += LETTER[((LETTER.find(x)*k1)+k2)%len(LETTER)]
    return cipher

#### affineDecrypt
# input : cipher, k1, k2
# output : plaintext

def affineDecrypt(cipher, k1, k2):
    plaintext = ''
    for x in cipher:
        c = LETTER.find(x)
        plain = ((c-k2)*modinv_2ndVer(k1, len(LETTER))) % len(LETTER)
        plaintext += LETTER[plain]
    return plaintext

def isPrime(n):
    for x in range(2,n):
        if (n % x) == 0:
            return False

    return True


#### RSA Encryption/Decryption

import random

keySize = 16   #bit

def genPrimeNum(keySize):
    while True:
        p = random.randrange(2**(keySize-1), 2**keySize)
        if isPrime(p):
            break
    return p

def genRSAKey(keySize):
    p = genPrimeNum(keySize)
    q = genPrimeNum(keySize)
    n = p * q
    while True:
        e = random.randrange(1, (p-1)*(q-1))
        if gcd(e, (p-1)*(q-1)) ==1:
            break
    d = findModInverse(e, (p-1)*(q-1))
    publicKey = (n, e)
    privateKey = (n, d)
    return publicKey, privateKey


pubKey, priKey = genRSAKey(16)
n,e = pubKey
d = priKey

print("public key n, e:", n, " ", e)
print("private key d:", d)

##############

LETTER = string.ascii_uppercase + string.ascii_lowercase + " "


def RSAEncrypt(msg, publicKey):
    cipherList = []
    n, e = publicKey
    for x in msg:
        p = LETTER.find(x)
        c = pow(p, e, n)
        cipherList.append(c)  # cipherList += [c]

    return cipherList


def RSADecrypt(cipherList, privateKey):
    output = ''
    n, d = privateKey
    for x in cipherList:
        plain = pow(x, d, n)
        output += LETTER[plain]

    return output


msg = input('Please enter a message for RSA Encryption: ')
pubKey, priKey = genRSAKey(16)
cipher = RSAEncrypt(msg, pubKey)
print(cipher)
plaintext = RSADecrypt(cipher, priKey)
print(plaintext)
if msg == plaintext:
    print("Decrypted Correctly")
else:
    print("Incorrect!!")


###### Caesar Cipher Brute Force Attack

LETTER = string.ascii_uppercase + string.ascii_lowercase + " "

def loadFile():
    dictionaryFile = open('dictionary.txt')
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = None
    dictionaryFile.close()
    return englishWords


def isEnglishStatement(msg, percentage=20):
    ENGLISH_WORDS = loadFile()
    possibleWords = msg.upper().split()
    if possibleWords == []:
        return 0.0  # no words at all, so return 0.0

    matches = 0
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            matches += 1

    if (float(matches) / len(possibleWords)*100) >= percentage:
        return True
    else:
        return False


msg = 'Hello World'

cipherCaesar = CaesarEnc(msg, 5)
print(cipherCaesar)

# 아래와 같은 코드를 이용해서 자동 검출
# import detectEnglish
#
# for key in range(1, 26):
#     decryptedMSG = CaesarDec(cipherCaesar, key)
#     print(decryptedMSG)
#     if detectEnglish.isEnglish(decryptedMSG):
#         print("found key:", key)
#         break


for key in range(1, len(LETTER)):
    decryptedMSG = CaesarDec(cipherCaesar, key)
    print(decryptedMSG)
    if isEnglishStatement(decryptedMSG):
        print("found key:", key)
        break

###### Affin Cipher Brute Force Attack

LETTER = string.ascii_uppercase + string.ascii_lowercase + " "

import detectEnglish

msg = 'Hello World Information Security Class'

cipherAffine = affineEncrypt(msg, 5, 7)
print(cipherAffine)

KeyList = []
for key in range(len(LETTER)):
    if gcd(key, len(LETTER))==1:
        KeyList.append(key)
print(KeyList)
print("Affine Cipher Hack with Dictionary!!")
for key1 in KeyList:
    for key2 in range(len(LETTER)):
        decMsg = affineDecrypt(cipherAffine, key1, key2)
        if (detectEnglish.isEnglish(decMsg.upper())):
            print("Key1:", key1, "Key2:", key2, "MSG:", decMsg)
            break

########## Hash

import hashlib

print(hashlib.algorithms_available)
print(hashlib.algorithms_guaranteed)

hash_object = hashlib.md5(b'Hello World')
print(hash_object.hexdigest(), "bit:", len(hash_object.hexdigest())*4)

mystring = input('Enter String to hash: ')
# Assumes the default UTF-8
hash_object = hashlib.md5(mystring.encode('utf-8'))
print(hash_object.hexdigest())

hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)

hash_object = hashlib.sha512(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)

import uuid

def hash_password(password):
    # uuid is used to generate a random number
    #salt = uuid.uuid4().hex
    salt = 'random string'
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


new_pass = input('Please enter a password: ')
hashed_password = hash_password(new_pass)
print('The string to store in the db is: ' + hashed_password)
old_pass = input('Now please enter the password again to check: ')
if check_password(hashed_password, old_pass):
    print('You entered the right password')
else:
    print('I am sorry but the password does not match')


####### Construct Hash DB

import hashlib

letters = string.ascii_lowercase + string.digits

def randomString(stringLength=8):
    """Generate a random string of stringLength """
    return ''.join(random.choice(letters) for i in range(stringLength))

def constructHashDB(genCount, maxStringLength=8):
    HashDB = {}
    for stringLength in range(1, maxStringLength+1):
        for count in range(genCount+1):
            msg = randomString(stringLength)
            hash_object = hashlib.sha256(msg.encode())
            hex_dig = hash_object.hexdigest()
            HashDB[hex_dig] = msg
    return HashDB


###### SHA 256 Brute Force Attack
mystring = 'b9x'   # 찾고자 하는 password를 설정함
hash_object = hashlib.sha256(mystring.encode())
org_hex_dig = hash_object.hexdigest()

### method 1
### DB 구성에 따라 찾을 수도 있고, 못찾을 수도 있음
print()
SHA256HashDB = constructHashDB(len(letters)**len(mystring), len(mystring))
#print(SHA256HashDB)
if org_hex_dig in SHA256HashDB:
    print("Found by Method 1!!! (db Size: %d)" %(len(SHA256HashDB)))
    print("Hash Value:", org_hex_dig, "Password:", SHA256HashDB[org_hex_dig])
else:
    print("Not Found by Method 1!!! (db Size: %d)" %(len(SHA256HashDB)))

### method 2
### 찾을때 까지 무한 반복
print()
count =0
stringLength = len(mystring)
while True:
    msg = randomString(random.randrange(1,stringLength+1))
    hash_object = hashlib.sha256(msg.encode())
    hex_dig = hash_object.hexdigest()
    count +=1
    if org_hex_dig in hex_dig:
        print("Found by Method 2!!! (try: %d)" %(count))
        print("Hash Value:", org_hex_dig, "Password:", msg)
        break


###########
import hashlib
import string
LETTER = string.ascii_lowercase+string.ascii_uppercase+string.digits+" "+":"
key = 7
msg = 'Hello World'

msgWithHash = msg +"::"+hashlib.sha256(msg.encode()).hexdigest()

cipher = CaesarEnc(msgWithHash, key)
#########network transmit...

decryptedMSG = CaesarDec(cipher,key)
msgPart, hashPart = decryptedMSG.split('::')

if(hashlib.sha256(msgPart.encode()).hexdigest() == hashPart):
    print("Correct")
    print("Received msg:", msgPart )