from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
msg = b"test message"

priKey_Alice = RSA.import_key(open("private_key_MY.bin","rb").read())
signature_Alice = pkcs1_15.new(priKey_Alice)

msg_hash = SHA256.new(msg)
signature = signature_Alice.sign(msg_hash)
print("signature value: ",signature)
print("length of signature:", len(signature))

public_Key_Bob = RSA.import_key(open("public_key_Bob.bin","rb").read())
cipher_RSA_Alice = PKCS1_OAEP.new(public_Key_Bob)
enc_msg = cipher_RSA_Alice.encrypt(msg)

file_out = open("signature_And_enc_by_Alice.bin","wb")
file_out.write(signature + enc_msg)
file_out.close()

