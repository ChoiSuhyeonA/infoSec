from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# creation 256 bit session key
sessionkey = Random.new().read(32) # 256 bit

# encryption AES of the message
f = open('./Hybrid/sig_MSG_Alice.txt','rb')   ### signature.txt || plaintext
plaintext = f.read(); f.close()
iv = Random.new().read(16) # 128 bit
obj = AES.new(sessionkey, AES.MODE_CFB, iv)
ciphertext = iv + obj.encrypt(plaintext)

# encryption RSA of the session key
publickey = RSA.importKey(open('./Hybrid/bobpublickey.txt','rb').read())
cipherrsa = PKCS1_OAEP.new(publickey)
enc_sessionkey = cipherrsa.encrypt(sessionkey)
print("Length of encrypted session key: ", len(enc_sessionkey))  #### Length of session key: 256 byte
print("Encrypted Session Key:", enc_sessionkey)
f = open('./Hybrid/outputAlice.txt','wb')
f.write(bytes(enc_sessionkey));
f.write(bytes(ciphertext));
f.close()