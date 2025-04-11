import socket
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST = '127.0.0.1'
PORT = 8080

# Diffie-Hellman parameters
p, g, a = 7, 5, 3
A = g ** a % p

# Connect to server
sock = socket.socket()
sock.connect((HOST, PORT))

# Send Diffie-Hellman parameters and A to the server
sock.send(pickle.dumps((p, g, A)))

# Receive B from the server
msg = sock.recv(1024)
B = pickle.loads(msg)

# Calculate the shared secret K
K = B ** a % p
print("Shared secret K =", K)

# Receive the server's public key
msg = sock.recv(1024)
server_public_key = pickle.loads(msg)

# Encrypt a message using the server's public key
message = "Hello, server!"
encryptor = PKCS1_OAEP.new(server_public_key)
encrypted_message = encryptor.encrypt(message.encode())

# Send the encrypted message to the server
sock.send(pickle.dumps(encrypted_message))

sock.close()