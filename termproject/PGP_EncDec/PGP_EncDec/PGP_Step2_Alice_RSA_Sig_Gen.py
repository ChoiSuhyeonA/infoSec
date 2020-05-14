from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# creation of signature
f = open('./Hybrid/plaintext.txt','rb')
plaintext = f.read(); f.close()
privatekey = RSA.importKey(open('./Hybrid/aliceprivatekey.txt','rb').read())
myhash = SHA.new(plaintext)
signature_Function = pkcs1_15.new(privatekey)
signature = signature_Function.sign(myhash)
f = open('./Hybrid/signatureAlice.txt','wb')
f.write(bytes(signature)); f.close()
print("Length of Signature: ", len(signature))
print("Signature: ", signature)
output = signature + plaintext  ## concatnate message
f = open('./Hybrid/sig_MSG_Alice.txt','wb')
f.write(bytes(output)); f.close()