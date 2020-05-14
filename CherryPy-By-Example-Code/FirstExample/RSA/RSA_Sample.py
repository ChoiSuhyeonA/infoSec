from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

# ================================================
# RSA Public_Key & Private_Key 생성 과정 (secret_code 설정)
print("******RSA Public_Key & Private_Key 생성 과정 (secret_code 설정)")

cipher_RSA = RSA.generate(2048)
private_key = cipher_RSA.export_key()
print(private_key)
file_out = open("private_key_MY.bin","wb")
file_out.write(private_key)
file_out.close()

public_key = cipher_RSA.publickey().export_key()
print(public_key)
file_out = open("public_key_MY.bin","wb")
file_out.write(public_key)
file_out.close()
# ================================================
#Bob
cipher_RSA_Bob = RSA.generate(2048)
private_key_Bob = cipher_RSA_Bob.export_key()
file_out = open("private_key_Bob.bin","wb")
file_out.write(private_key_Bob)
file_out.close()

public_key_Bob = cipher_RSA_Bob.publickey().export_key()
file_out = open("public_key_Bob.bin","wb")
file_out.write(public_key_Bob)
file_out.close()

# ================================================
# 생성된 RSA Public_Key 읽어들이는 과정 (Alice ...)

file_in = open("public_key_My.bin","rb")
public_key_bob = file_in.read()

cipher_RSA = RSA.import_key(public_key_bob)
pub_key_bob = cipher_RSA.export_key() # 시스템에서 만들어진 키를 보여주는 것 export_key
recipient_public_key = RSA.import_key(public_key_bob)
cipher_rsa = PKCS1_OAEP.new(recipient_public_key)