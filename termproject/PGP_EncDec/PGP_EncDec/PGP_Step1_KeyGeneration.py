from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# key generation Alice
privatekey = RSA.generate(2048)
f = open('./Hybrid/aliceprivatekey.txt','wb')
f.write(bytes(privatekey.exportKey('PEM'))); f.close()
publickey = privatekey.publickey()
f = open('./Hybrid/alicepublickey.txt','wb')
f.write(bytes(publickey.exportKey('PEM'))); f.close()

# key generation Bob
privatekey = RSA.generate(2048)
f = open('./Hybrid/bobprivatekey.txt','wb')
f.write(bytes(privatekey.exportKey('PEM'))); f.close()
publickey = privatekey.publickey()
f = open('./Hybrid/bobpublickey.txt','wb')
f.write(bytes(publickey.exportKey('PEM'))); f.close()