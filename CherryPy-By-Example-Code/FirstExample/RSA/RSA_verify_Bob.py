from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

msg_from_Alice = open("signature_by_Alice.bin","rb").read()

sig_part = msg_from_Alice[:256]
msg_part = msg_from_Alice[256:]#+ b"ttt"넣으면 incorrect가 뜬다.
pubkey_Alice = RSA.import_key(open("private_key_MY.bin","rb").read())
signature_Bob = pkcs1_15.new(pubkey_Alice)

msg_hash = SHA256.new(msg_part)
try:
    signature_Bob.verify(msg_hash,sig_part)
    print("Correct Signature !! Received message = ",msg_part)
except:
    print("Incorrect")