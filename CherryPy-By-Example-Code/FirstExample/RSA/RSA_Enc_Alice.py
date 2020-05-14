from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
### public_key_Bob.bin 만 있다고 가정...
file_in = open("public_key_Bob.bin","rb")
temp = file_in.read()
file_in.close()

pubkey_Bob = RSA.import_key(temp)  # 수신자(Bob)의 public_key를 읽어들임
### cipher_RSA = RSA.generate(2048) 하는게 아니라..
cipher_RSA = PKCS1_OAEP.new(pubkey_Bob) # 수신자(Bob)의 public_key를 이용하여 RSA Cipher를 생성함
message = b"test message"
enc_msg = cipher_RSA.encrypt(message) # RSA Cipher를 이용하여 메시지에 대한 암호문 생성
print(enc_msg)
file_out = open("encrypted_data_from_Alice_to_Bob.bin", "wb")
file_out.write(enc_msg)
file_out.close()
print("Alice가 Bob에게 전송하고자 하는 파일 'encrypted_data_from_Alice_to_Bob.bin'이 생성됨")






