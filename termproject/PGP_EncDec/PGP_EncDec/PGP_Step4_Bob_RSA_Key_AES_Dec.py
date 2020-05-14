from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

ENC_SESSION_KEY_SIZE = 256   # 256 * 8 = 2048 bit

f = open('./Hybrid/outputAlice.txt','rb')   ### signature.txt || plaintext
outputAlice = f.read(); f.close()

# decryption session key
privatekey = RSA.importKey(open('./Hybrid/bobprivatekey.txt','rb').read())
cipherrsa = PKCS1_OAEP.new(privatekey)

sessionkey = cipherrsa.decrypt(outputAlice[:ENC_SESSION_KEY_SIZE])
ciphertext = outputAlice[ENC_SESSION_KEY_SIZE:]

iv = ciphertext[:16]
obj = AES.new(sessionkey, AES.MODE_CFB, iv)
plaintext = obj.decrypt(ciphertext[16:])
f = open('./Hybrid/sig_MSG_Bob.txt','wb')
f.write(bytes(plaintext)); f.close()