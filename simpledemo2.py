import  string
LETTER = string.ascii_letters
print(LETTER)

def CaesarEnc(message,key1, key2):
    cipher =''
    for x in message:
        cipher += LETTER[((LETTER.find(x) * key1)+key2) % len(LETTER)]
    return cipher
    #print(result)
def CaesarDec(cipher,key1, key2):
    plaintext =''
    for x in cipher:
        plaintext+= LETTER[((LETTER.find(x) - key2)/key1) % len(LETTER)]
        return plaintext
    #print(plaintext)

    #__main__#
message = 'ABCDXYZ'
key1 = 7
key2 = 3
print("message", message, "\nkey1", key1, "\nkey2", key2)
ciphertext = CaesarEnc(message,key1, key2)
print(ciphertext)
plainText = CaesarDec(ciphertext,key1, key2)
print(plainText)

