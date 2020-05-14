from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import socket                   # Import socket module
import base64
from Crypto.Cipher import AES
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


# Step 0 : Bob Generation key of Bob
privatekey = RSA.generate(2048)
f = open('./HybridBob/bobprivatekey.txt','wb')
f.write(bytes(privatekey.exportKey('PEM'))); f.close()
publickey = privatekey.publickey()
f = open('./HybridBob/received_bobpublickey.txt','wb')
f.write(bytes(publickey.exportKey('PEM'))); f.close()



# Step 1-1 : Receive Alice's Public Key
client_socket_C = socket.socket()             # Create a socket object
host = 'localhost'     # Get local machine name
port = 10005              # Reserve a port for your service.

client_socket_C.connect((host, port))
client_socket_C.send(b"Client OK")

f = open('./HybridBob/received_alicepublickey.txt', 'wb')
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


# Step 1-2 : Bob Transfer Public Key
port = 10006                    # Reserve a port for your service.
server_socket = socket.socket()             # Create a socket object
host = 'localhost'              # Get local machine name
server_socket.bind((host, port))            # Bind to the port
server_socket.listen(5)                     # Now wait for client connection.

print('Server listening....')

while True:
    client_socket_S, addr = server_socket.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = client_socket_S.recv(1024)
    print('Server received', repr(data))

    filename='./HybridBob/received_bobpublickey.txt'
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

print("*******************************************")

# Step 3-2 :
host = 'localhost'     # Get local machine name
port = 10002              # Reserve a port for your service.
client_socket = socket.socket()             # Create a socket object
client_socket.connect((host, port))
client_socket.send(b"Client OK")

f = open('./HybridBob/b64_received_outputAlice.txt', 'wb')
print('file opened')

while True:
    print('receiving data...')
    data = client_socket.recv(1024)     # sender : 3 * 256 = 768 byte --> b64 Encoding --> 4 * 256 = 1024 byte
    data = base64.b64decode(data)       # write decoded data to f
    if not data:
        break
    f.write(data)
    print('length of received data: ', len(data))

f.close()
print('Successfully get the file')
client_socket.close()
server_socket.close()
print('connection closed')


fromFile = './HybridBob/b64_received_outputAlice.txt'
toFile = './HybridBob/received_outputAlice.txt'


def B64Decoding(fromFile, toFile):
    ff = open(fromFile, 'rb')
    l = ff.read(1024)   # 4byte * 256 = 1024
    tf = open(toFile, 'wb')
    while(l):
        l = base64.b64decode(l)
        tf.write(l)
        l = ff.read(1024)
    tf.close()
    ff.close()

B64Decoding(fromFile, toFile)

# Step 4 :
ENC_SESSION_KEY_SIZE = 256   # 256 * 8 = 2048 bit

f = open('./HybridBob/received_outputAlice.txt','rb')   ### signature.txt || plaintext
outputAlice = f.read(); f.close()

# decryption session key
privatekey = RSA.importKey(open('./HybridBob/bobprivatekey.txt','rb').read())
cipherrsa = PKCS1_OAEP.new(privatekey)

sessionkey = cipherrsa.decrypt(outputAlice[:ENC_SESSION_KEY_SIZE])
ciphertext = outputAlice[ENC_SESSION_KEY_SIZE:]

iv = ciphertext[:16]
obj = AES.new(sessionkey, AES.MODE_CFB, iv)
plaintext = obj.decrypt(ciphertext[16:])
f = open('./HybridBob/sig_MSG_Bob.txt','wb')
f.write(bytes(plaintext)); f.close()



# Step 5 :
# decryption signature
f = open('./HybridBob/sig_MSG_Bob.txt','rb')
sig_MSG = f.read(); f.close()

publickey = RSA.importKey(open('./HybridBob/received_alicepublickey.txt','rb').read())
cipherrsa = PKCS1_v1_5.new(publickey)

print("Signature: ", sig_MSG[:256])
print("PlainText: ", sig_MSG[256:])

myhash = SHA.new(sig_MSG[256:])
result = cipherrsa.verify(myhash, sig_MSG[:256])
print("Signature Verification Result : ", result)
