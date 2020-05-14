import string, random
from cryptomath import gcd, findModInverse
from detectEnglish import isEnglish

# input : LETTERS, plaintext, key
# output : ciphertext
def caesarEnc(LETTERS, plaintext, key):
    ciphertext =''
    for c in plaintext:
        if c in LETTERS:
            ciphertext += LETTERS[(LETTERS.find(c) + key) % len(LETTERS)]
        else:
            ciphertext += c
    return ciphertext

# input : LETTERS, ciphertext, key
# output : plaintext
def caesarDec(LETTERS, ciphertext, key):
    plaintext = ''
    for c in ciphertext:
        if c in LETTERS:
            plaintext += LETTERS[(LETTERS.find(c) - key) % len(LETTERS)]
        else:
            plaintext += c
    return plaintext

# input : LETTERS, ciphertext, ????
# output : decrypted plaintext (콘솔에 출력)
def caesarHack(LETTERS, ciphertext):
    for key in range(len(LETTERS)):
        plaintext = caesarDec(LETTERS, ciphertext, key)
        print("Key:", key, " DecPlaintext:", plaintext)

# input : LETTERS
# output : RRS Z*_letter
def findReducedResidueSet(LETTERS):
    RRS = []  #기약잉여류집합...
    for c in range(1,len(LETTERS)):
        if (gcd(c, len(LETTERS)) == 1): # 서로소인 원소
            RRS.append(c)
    return RRS

# input : LETTERS, plaintext, key1, key2
# output : ciphertext
def affineEnc(LETTERS, plaintext, key1, key2):
    ciphertext = ""
    for c in plaintext:
        if c in LETTERS:
            ciphertext += LETTERS[((LETTERS.find(c)*key1)+key2)%len(LETTERS)]
        else:
            ciphertext += c
    return ciphertext

def affineEnc2(LETTERS, plaintext, key1, key2):
    ciphertext = []
    for c in plaintext:
        if c in LETTERS:
            ciphertext += LETTERS[((LETTERS.find(c)*key1)+key2)%len(LETTERS)]
        else:
            ciphertext += c
    return ''.join(ciphertext)

# input : LETTERS, ciphertext, key1, key2
# output : plaintext
def affineDec(LETTERS, ciphertext, key1, key2):
    plaintext = ""
    for c in ciphertext:
        if c in LETTERS:
            plaintext += LETTERS[( (LETTERS.find(c)-key2)*findModInverse(key1, len(LETTERS)) )%len(LETTERS)]
        else:
            plaintext += c
    return plaintext

# input : LETTERS, affineCipher, ???, ???
# output : decrypted plaintext (콘솔에 출력)
def affineHack(LETTERS, ciphertext):
    guessed_RRS = findReducedResidueSet(LETTERS)

    for key1 in guessed_RRS:
        for key2 in range(0, len(LETTERS)):
            guessed_plaintext = affineDec(LETTERS, ciphertext, key1, key2)
            print("key1: %d  key2: %d  plaintext: %s" %(key1, key2, guessed_plaintext))

def affineHackAutoDetect(LETTERS, ciphertext):
    guessed_RRS = findReducedResidueSet(LETTERS)
    for key1 in guessed_RRS:
        for key2 in range(0, len(LETTERS)):
            guessed_plaintext = affineDec(LETTERS, ciphertext, key1, key2)
            if isEnglish(guessed_plaintext, 50):
                print("key1: %d  key2: %d  plaintext: %s" %(key1, key2, guessed_plaintext))
                return 1
    return 0

# input : Length (문자집합의 개수??)
# output : LETTERS
def GenLETTERS(Length):
    LETTERS = ""
    specialCharSet ="!@#$%^&*()_+={[}];:<>?/"
    LETTERSET = string.digits + specialCharSet
    RandLength = Length #random.randint(0, Length)
    # LETTERS = ''.join(random.choice(LETTERSET) for x in range(RandLength)) #random.choice(스트링) 함수는 스트링 중에 하나 뽑는것
    #                                                                        #for문 만큼 반복
    for i in range(RandLength):
        LETTERS += random.choice(LETTERSET)                                #위에꺼랑 같은 표현(맨 윗줄 LETTERS = "" 해줘야 됨)
    return string.ascii_letters + LETTERS

if __name__ =="__main__":
    LETTERS = string.ascii_letters + "$%"
    # LETTERS = GenLETTERS(52)
    print(LETTERS)
    plaintext ="this is an information security class 2019$. Hanshin University%"
    #plaintext = "fdjlf fdljfpg grepogj hjpthj fgpgjg fgdg"
    print("Plaintext:", plaintext)
    key = random.randrange(0,len(LETTERS))
    print("Selected Key:", key)
    ciphertext = caesarEnc(LETTERS, plaintext, key)
    print("Ciphertext:", ciphertext)

    #plaintext2 = caesarDec(LETTERS, ciphertext, key)
    #print("Plaintext:", plaintext2)

    #LETTERS를 알고 있다는 가정..
    #LETTERS = string.ascii_letters + ".+*/$"
    #LETTERS = string.ascii_uppercase
    #ciphertext = "R UXEN VH TRCCH"
    caesarHack(LETTERS, ciphertext)

    # Affine Enc / Dec
    RRS = findReducedResidueSet(LETTERS)

    key1 = RRS[random.randrange(0,len(RRS))]
    print(key1)
    key2 = random.randrange(0, len(LETTERS))
    print(key2)

    #LETTERS = "t4h#is$"
    #plaintext = "this is"

    affineCipher = affineEnc(LETTERS, plaintext, key1, key2)
    print(affineCipher)

    #affinePlaintext = affineDec(LETTERS, affineCipher, key1, key2)
    #print(affinePlaintext)

    # LETTERS 집합은 알고 있다는 가정... affineCipher는 주어짐.
    #affineHack(LETTERS, affineCipher)

    # LETTERS 집합을 모른다?? affineCipher는 주어짐.

    while(True):
        LETTERS = GenLETTERS(2)         # $% 두개 main 맨위
        print("Generated LETTERS:", LETTERS)
        status = affineHackAutoDetect(LETTERS, affineCipher)
        if status == 1:
            break