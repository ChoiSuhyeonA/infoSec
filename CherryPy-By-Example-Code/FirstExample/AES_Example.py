from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto import Random
import base64
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = AES.block_size
KEY_SIZE = AES.key_size[2]

key = get_random_bytes(KEY_SIZE)
print(key)
print(len(key))
IV = Random.new().read(BLOCK_SIZE)
plaintext = "Information Security with Python...."


cipher = AES.new(key, AES.MODE_CFB, IV)
print(cipher)
enc_msg = cipher.encrypt(plaintext.encode())
print("암호화된 메시지: ",enc_msg)
print("base64를 이용해 인코딩한 메시지: ",base64.b32encode(enc_msg))
print("인코딩한 메시지를 디코딩한 메시지: ",base64.b32encode(enc_msg).decode())

enc_msg_base64 = base64.b32encode(enc_msg).decode()

cipher = AES.new(key, AES.MODE_CFB, IV)
dec_msg = cipher.decrypt(base64.b32decode(enc_msg_base64.encode()))
temp = base64.b32decode(enc_msg_base64.encode())
#print(enc_msg)
#print(temp)
if(enc_msg == temp):
    print("same")

print("복호화한 메시지(binary): ",dec_msg)
print("복호화된 메시지(string): ",dec_msg.decode())

def AES_Enc(key, message):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    return base64.b32encode(cipher.encrypt(pad(message.encode(),16))).decode()

def AES_Dec(key, message):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(base64.b32decode(message_out.encode())),16).decode()

def OTHER_BLOCK_CIPHER_ENC(message):
    pad_r = len(message)

    if (pad_r % 16 != 0):
        tmp = 16 - pad_r
        for i in range(0, tmp):
            message += '*'
    return message

message = "Python programming on Security programming class...."
          #cfb는 길이에 상관이 없지만, cbc ofb 등등은 16의 배수, 따라서 pad, unpad 를 사용한다.

message_out = AES_Enc(key,message)
print("암호문: ",message_out)
print("복호문: ",AES_Dec(key, message_out))