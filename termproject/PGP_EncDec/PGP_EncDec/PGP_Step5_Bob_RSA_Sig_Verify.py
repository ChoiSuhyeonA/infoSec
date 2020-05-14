from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# decryption signature
f = open('./Hybrid/sig_MSG_Bob.txt','rb')
sig_MSG = f.read(); f.close()

publickey = RSA.importKey(open('./Hybrid/alicepublickey.txt','rb').read())
cipherrsa = pkcs1_15.new(publickey)

print("Signature: ", sig_MSG[:256])
print("PlainText: ", sig_MSG[256:])

f = open("./Hybrid/received_plaintext.txt","wb")
f.write(sig_MSG[256:]); f.close()

myhash = SHA.new(sig_MSG[256:])

# pycryptodome으로 변경하고 아래와 같이 수정함
#result = cipherrsa.verify(myhash, sig_MSG[:256])
#print("Signature Verification Result : ", result)

try:
    pkcs1_15.new(publickey).verify(myhash, sig_MSG[:256])
    # 검증 결과 이상이 없으면 None 값이 리턴되고, 오류가 있는 경우 except 문 실행함...
    print("Signature Verification Result : True")
except (ValueError, TypeError):
    print("Signature Verification Result : False")