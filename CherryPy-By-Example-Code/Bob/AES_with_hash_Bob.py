from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
import base64
BLOCK_SIZE = 16
KEY_SIZE = 32

BLOCK_SIZE = AES.block_size
KEY_SIZE = AES.key_size[2]


#Bob
#두개의 파일을 받았다고 가정....
file_in = open("enc_key.bin","rb")
IV_with_enc_key = file_in.read()
file_in.close()
IV2 = IV_with_enc_key[:16]
enc_key_part = IV_with_enc_key[16:]
print("Received IV: ",IV2)

priKey_Bob = RSA.import_key(open("private_key_Bob.bin","rb").read())
cipher_RSA_Bob = PKCS1_OAEP.new(priKey_Bob)
key2 = cipher_RSA_Bob.decrypt(enc_key_part)

print("Received key: ",key2)

file_in = open("enc_msg.bin","rb")
enc_msg_bob = file_in.read()
file_in.close()

cipher_Bob = AES.new(key2, AES.MODE_CBC, IV2)

msg_with_hash_Bob = unpad(cipher_Bob.decrypt(base64.b32decode(enc_msg_bob)), AES.block_size)
print(msg_with_hash_Bob)
hash_part = msg_with_hash_Bob[:32] #SHA256.digest_size == 32bytes
msg_part = msg_with_hash_Bob[32:]

hash_Bob = SHA256.new(msg_part)
if hash_part == hash_Bob.digest():
    print("Correct!!")
    print("Received msg: ",msg_part)
else:
    print("error!!")