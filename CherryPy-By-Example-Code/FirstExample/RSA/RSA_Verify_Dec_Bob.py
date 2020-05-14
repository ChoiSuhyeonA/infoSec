from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP

msg_from_Alice = open("signature_And_enc_by_Alice.bin","rb").read()

sig_part = msg_from_Alice[:256]
enc_msg_part = msg_from_Alice[256:]#+ b"ttt"넣으면 incorrect가 뜬다.

#Bob이 자신의 private key를 이용하여 암호화 된 메시지를 복호화..
prikey_Bob = RSA.import_key(open("private_key_Bob.bin","rb").read())
cipher_RSA_Bob = PKCS1_OAEP.new(prikey_Bob)
msg_part = cipher_RSA_Bob.decrypt(enc_msg_part)

#Bob이 Alice의 공개키를 이용해서 서명 부분을 확인..
pubkey_Alice = RSA.import_key(open("private_key_MY.bin","rb").read())
signature_Bob = pkcs1_15.new(pubkey_Alice)

msg_hash = SHA256.new(msg_part)
try:
    signature_Bob.verify(msg_hash,sig_part)
    print("Correct Signature !! Received message = ",msg_part)
except:
    print("Incorrect")