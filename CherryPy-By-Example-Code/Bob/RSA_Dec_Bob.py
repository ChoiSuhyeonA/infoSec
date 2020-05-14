###(RSA_Dec_Bob.py 코드의 전체적인 작동 과정)
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

###1. Bob 자산의 Private_key 파일(Private_key_Bob.bin)을 읽어들임
file_in = open("private_key_Bob.bin","rb")
temp = file_in.read()
file_in.close()

###2. 읽어들인 파일을 이용하여 cipher_RSA를 만듬
cipher_RSA = PKCS1_OAEP.new(RSA.import_key(temp))

###3. Alice로 부터 받은 파일('encrypted_data_from_Alice_to_Bob.bin')을 읽어들임
file_in = open("encrypted_data_from_Alice_to_Bob.bin", "rb")
try:
    enc_data = file_in.read()
except:
    print("Without enc_data!!")
file_in.close()

###4. cipher_RSA를 이용하여  encrypted_data_from_Alice_to_Bob.bin 내용을 복호화함
dec_msg = cipher_RSA.decrypt(enc_data)
print("복호화가 완료된 메시지: ",dec_msg)
print(dec_msg.decode())

