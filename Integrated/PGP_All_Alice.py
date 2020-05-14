from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import socket                   # Import socket module
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64
from Crypto.Cipher import AES
from Crypto import Random


# Step 0 : Alice Generation Key of Alice
privatekey = RSA.generate(2048)
f = open('./HybridAlice/aliceprivatekey.txt','wb')
f.write(bytes(privatekey.exportKey('PEM'))); f.close()
publickey = privatekey.publickey()
f = open('./HybridAlice/received_alicepublickey.txt','wb')
f.write(bytes(publickey.exportKey('PEM'))); f.close()


# Step 1-1 : Alice(Server) Transfer Public Key
port = 10005                    # Reserve a port for your service.
host = 'localhost'              # Get local machine name
server_socket = socket.socket()             # Create a socket object
server_socket.bind((host, port))            # Bind to the port
server_socket.listen(5)                     # Now wait for client connection.

print('Server listening....')

while True:
    client_socket_S, addr = server_socket.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = client_socket_S.recv(1024)
    print('Server received', repr(data))

    filename='./HybridAlice/received_alicepublickey.txt'
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       client_socket_S.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()
    print('Done sending')
    client_socket_S.send(b'')
    break
client_socket_S.close()
server_socket.close()



# Step 1-2 : Receive Bob's Public Key
host = 'localhost'     # Get local machine name
port = 10006              # Reserve a port for your service.
client_socket_C = socket.socket()             # Create a socket object
client_socket_C.connect((host, port))
client_socket_C.send(b"Client OK")

f = open('./HybridAlice/received_bobpublickey.txt', 'wb')
print('file opened')

while True:
    print('receiving data...')
    data = client_socket_C.recv(1024)
    print('data=', data.decode('utf-8'))
    if not data:
        break
    f.write(data)

f.close()
print('Successfully get the file')
client_socket_C.close()
print('connection closed')



# Step 2 : Alice Generate RSA Signature
# creation of signature
f = open('./HybridAlice/plaintext.txt','rb')
plaintext = f.read(); f.close()
privatekey = RSA.importKey(open('./HybridAlice/aliceprivatekey.txt','rb').read())
myhash = SHA.new(plaintext)  # Generate Hash
signature = PKCS1_v1_5.new(privatekey)   # Signature algo
sigVal = signature.sign(myhash)   # signature value
print("Length of Signature: ", len(sigVal))
print("Signature: ", sigVal)
output = sigVal + plaintext  ## concatnate message
f = open('./HybridAlice/sig_MSG_Alice.txt','wb')
f.write(bytes(output)); f.close()



# Step 3 :
# creation 256 bit session key
sessionkey = Random.new().read(32) # 256 bit

# encryption AES of the message
f = open('./HybridAlice/sig_MSG_Alice.txt','rb')   ### signature.txt || plaintext
plaintext = f.read(); f.close()
iv = Random.new().read(16) # 128 bit
obj = AES.new(sessionkey, AES.MODE_CFB, iv)
ciphertext = iv + obj.encrypt(plaintext)

# encryption RSA of the session key
publickey = RSA.importKey(open('./HybridAlice/received_bobpublickey.txt','rb').read())
cipherrsa = PKCS1_OAEP.new(publickey)
enc_sessionkey = cipherrsa.encrypt(sessionkey)
print("Length of encrypted session key: ", len(enc_sessionkey))  #### Length of session key: 256 byte
print("Encrypted Session Key:", enc_sessionkey)
f = open('./HybridAlice/outputAlice.txt','wb')
f.write(bytes(enc_sessionkey))
f.write(bytes(ciphertext))
f.close()

print("*******************************************")


# Step 3-1 : Alice Send Encrypted File to Bob...
fromFile = './HybridAlice/outputAlice.txt'
toFile = './HybridAlice/b64_outputAlice.txt'


def B64Encoding(fromFile, toFile):
    ff = open(fromFile, 'rb')
    l = ff.read(768)   # 3byte * 256 = 768
    tf = open(toFile, 'wb')
    while(l):
        l = base64.b64encode(l)
        tf.write(l)
        l = ff.read(768)
    tf.close()
    ff.close()

B64Encoding(fromFile, toFile)

port = 10002                    # Reserve a port for your service.
host = 'localhost'              # Get local machine name
server_socket = socket.socket()             # Create a socket object
server_socket.bind((host, port))            # Bind to the port
server_socket.listen(5)                     # Now wait for client connection.

print('Server listening....')

while True:
    client_socket, addr = server_socket.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = client_socket.recv(1024)
    print('Server received', repr(data))

    #filename='./Hybrid/received_alicepublickey.txt'
    filename = toFile
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       client_socket_S.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()
    print('Done sending')
    client_socket_S.send(b'')
    break
client_socket.close()
server_socket.close()