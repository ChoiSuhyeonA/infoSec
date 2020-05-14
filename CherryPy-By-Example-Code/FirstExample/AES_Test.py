from Crypto import Random
from Crypto.Cipher import AES
import os
import base64

BLOCK_SIZE = 16
KEY_SIZE=32
key = Random.new().read(KEY_SIZE)
#key = os.urandom(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

message = "Information Security & Programming. Test Message!...."# binary code로 encode 해주어야 한다.
print("key: ", key)
print("key length: ", len(key))

def AESencrypt(message, passphrase):
    cipher = AES.new(passphrase, AES.MODE_CFB, IV)
    print(cipher)
    return cipher.encrypt(message.encode())

def AESdecrypt(encrypted, passphrase): # passphrase = key
    cipher = AES.new(passphrase, AES.MODE_CFB, IV)
    return cipher.decrypt(encrypted)

encrypted = AESencrypt(message, key)
print("Encrypted: ", encrypted)
print("Encrypted (base64): ", base64.b32encode(encrypted))
print("Encrypted (base64 & decode): ", base64.b32encode(encrypted).decode())

decrypted = AESdecrypt(encrypted, key)
print("Decrypted: ", decrypted.decode('utf-8'))
