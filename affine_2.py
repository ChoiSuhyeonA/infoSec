# 암호문 = (p x k1) +k2 ) mod 26
# 평문  = (c-k2) * k1(역원)) mod 26
# 아핀 암호 생성기 만들기(역원 생성기 코드 찾아서 이용)

import string, random
LETTER = string.ascii_uppercase + string.ascii_lowercase + " "

#모튤러 연산

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


#모듈러 연산 2
def modinv2(a, m):
    if gcd(a,m) != 1:
        raise Exception('modular inverse does not exist')
    else:
        return pow(a,eularPhi(m)-1,m)


#암호화 기능

def ApinEnc(message,key1,key2):
    cypertext = ''
    for x in message:
        num = LETTER.find(x)
        cypertext += LETTER[((num * key1)+key2) % len(LETTER)]
    return cypertext


#복호화 기능

def ApinDec(cyper, key1,key2):
    plaintext = ''
    for y in cyper:
        num = LETTER.find(y)
        plaintext += LETTER[((num - key2)*modinv2(key1,len(LETTER))) % len(LETTER)]
    return plaintext

#gcd
def gcd(a,b):
    while a != 0:
        a,b = b % a,a
    return b

#오일러 파이(n) 구하는 함수

def eularPhi(n):
    phi = []
    x = 1
    while x<n:
        if gcd(x,n) == 1:
            phi +=[x] #phi.append(x)
        x += 1

    return len(phi)

def gcd(a,b):
    while a!= 0:
        a,b = b%a, a
    return b

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

def eularPhi(n):
    phi = []
    x =1
    while x<n:
        if gcd(x,n) ==1:
            phi +=[x]  #phi append x.
        x += 1
    return len(phi)

def modinv_(a,m):
    if gcd(a,m) != 1:
        return None
    else:
        return pow(a, eularPhi(m)-1,m)


###MAIN###

print("암호문 입력 하십시오 : ",end='')
message = input()

print("키1 를 입력 하십시오 : ",end='')
key1 = int(input())

print("키3 를 입력 하십시오 : ",end='')
key2 = int(input())

cypertext = ApinEnc(message,key1,key2)

print('암호문 : ' + cypertext)

plaintext = ApinDec(cypertext,key1,key2)

print('평문 : ' + plaintext)



print(e)


n=p*q
e=157

keySize = 16
def genPrimeNum(keySize):
    while True:
        e = random.randrange(2**(keySize-1),(p-1)*(q-1))
        if gcd(e, (p-1)*(q-1)):
            break
       # if isPrime(p):
          #  break
p= genPrimeNum(16)
q= genPrimeNum(16)

d = find
d = modinv_(e, eularPhi(n))
print("public key n,e: ", n," ",e)
print("private key d: ", d)

p=3
c = pow(p,e,n)
print("Ciphertext c: ", c)

plain = pow(c,d,n)
print("Plaintext p",plain)

def isPrime(n):
    for x in range(2,n):
        if(n%x) ==0:
            return False

        return True



msg = 'HANSHIN'
MSG = 'Hello World'
cipherList = []
for x in msg:
    p = LETTER.find(x)
    c = pow(p, e, n)
    print(c)
    cipherList += [c]

print(ciperList)

output=''
for x in cipherList:
   # print(x)
    plain = pow(x, d, n)

    output += LETTER[plain]

print(output)

