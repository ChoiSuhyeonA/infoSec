from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
BLOCK_SIZE = 16
KEY_SIZE = 32

BLOCK_SIZE = AES.block_size
KEY_SIZE = AES.key_size[2]

#Alice, Bob 이 공유하는 키/iv
key = Random.new().read(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

print("key: ",key)

#Alice
msg = "hello world!! Brother...."
hash = SHA256.new(msg.encode())
hashresult = hash.digest()
print(hashresult)
msg_with_hash = hashresult + msg.encode()
print(msg_with_hash)
cipher_AES_Alice = AES.new(key, AES.MODE_CBC, IV)
enc_msg = base64.b32encode(cipher_AES_Alice.encrypt(pad(msg_with_hash, AES.block_size))).decode()
# CBC/OFB/CTR 모드인 경우 패딩 수행 + base64 encoding
print("해쉬+평문에 대한 암호문 = ",enc_msg)
file_out = open("enc_msg.bin","wb")
file_out.write(enc_msg.encode())
file_out.close()

# Bob의 공개키를 이용해서 key,IV 값을 안전하게 전달.
pubKey_Bob = RSA.import_key(open("public_key_Bob.bin","rb").read())
cipher_RSA_Alice = PKCS1_OAEP.new(pubKey_Bob)
#IV_with_key = IV + key
enc_key = cipher_RSA_Alice.encrypt(key) #key는 바이트 형태이므로 encode 필요 없다.
file_out = open("enc_key.bin","wb")
file_out.write(IV + enc_key) #IV는 암호화 하지 않고 보낸다. AES에서 open하기 때문에, [:16]으로 잘라내면 된다.
file_out.close()