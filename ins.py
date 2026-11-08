'''
#---------------------Diffie------------------
#prime and generator
g=5
p=23
#priv keys
a=6
b=16
#public key
A=pow(g,a,p)
B=pow(g,A,p)
Ka=pow(g,B,p)
#secret keys
Ka=pow(g,B,p)
Kb=pow(g,B,p)

if Ka==Kb:
    print('success')
else:
    print('no')
'''
'''
#------------------hash256--------------
import hashlib
msg=input('enter msg:')
data=msg.encode('utf-8')
hash_val=hashlib.sha256(data).hexdigest()

print(hash_val)
'''
'''
#-------------


from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# Generate private and public keys
private_key = dsa.generate_private_key(key_size=2048)
public_key = private_key.public_key()

message = input("Enter the message: ").encode("utf-8")

# Generate digital signature using SHA-256
signature = private_key.sign(
    message,
    hashes.SHA256()
)

print("Original Message:", message.decode())
print("Digital Signature:", signature.hex())

# Verify the original message
try:
    public_key.verify(
        signature,
        message,
        hashes.SHA256()
    )
    print("Signature verified successfully!")
except InvalidSignature:
    print("Signature verification failed!")

# Verify a modified message
modified_message = message + b" modified"

try:
    public_key.verify(
        signature,
        modified_message,
        hashes.SHA256()
    )
    print("Modified message verified!")
except InvalidSignature:
    print("Modified message rejected!")

'''
'''
#-----------------------------caeser cipher---------------------
def encrypt(text, key):
    result = ""
    for ch in text:
        result += chr((ord(ch) + key) % 256)
    return result

def decrypt(text, key):
    result = ""
    for ch in text:
        result += chr((ord(ch) - key) % 256)
    return result

text = input("Enter plaintext: ")
key = int(input("Enter key: "))

cipher = encrypt(text, key)
print("Encrypted text:", cipher)
print("Decrypted text:", decrypt(cipher, key))
'''
'''
#-------------------------------playfair-----------------------------------------
def create_matrix(key):
    s = ""
    for ch in key.upper() + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch == 'J':
            ch = 'I'
        if ch not in s and ch.isalpha():
            s += ch
    return [list(s[i:i+5]) for i in range(0, 25, 5)]

def encrypt(text, m):
    text = text.upper().replace("J", "I").replace(" ", "")
    text = ''.join(c for c in text if c.isalpha())

    if len(text) % 2:
        text += 'X'

    result = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]

        if a == b:
            b = 'X'

        for r in range(5):
            for c in range(5):
                if m[r][c] == a:
                    r1, c1 = r, c
                if m[r][c] == b:
                    r2, c2 = r, c

        if r1 == r2:
            result += m[r1][(c1+1)%5] + m[r2][(c2+1)%5]
        elif c1 == c2:
            result += m[(r1+1)%5][c1] + m[(r2+1)%5][c2]
        else:
            result += m[r1][c2] + m[r2][c1]

    return result

key = input("Enter key: ")
text = input("Enter plaintext: ")

m = create_matrix(key)
cipher = encrypt(text, m)

print("Encrypted:", cipher)
print("Decrypted: Use the reverse rules (shift -1)")

#print(create_matrix('monarchy'))
'''
'''
#-------------------------------------hill cipher
import numpy as np

key = np.array([[3, 3], [2, 5]])
inv = np.array([[15, 17], [20, 9]])

text = input("Enter plaintext: ").upper().replace(" ", "")

if len(text) % 2:
    text += 'X'

def hill(text, matrix):
    result = ""
    for i in range(0, len(text), 2):
        p = np.array([[ord(text[i])-65],
                      [ord(text[i+1])-65]])
        c = np.dot(matrix, p) % 26
        result += chr(int(c[0][0])+65)
        result += chr(int(c[1][0])+65)
    return result

enc = hill(text, key)
print("Encrypted:", enc)
print("Decrypted:", hill(enc, inv))

'''
'''
#------------------------------------------rail fence
def encrypt(text, key):
    rail = [''] * key
    row, direction = 0, 1

    for ch in text:
        rail[row] += ch
        if row == 0:
            direction = 1
        elif row == key-1:
            direction = -1
        row += direction

    return ''.join(rail)

def decrypt(cipher, key):
    pattern = []
    row, direction = 0, 1

    for _ in cipher:
        pattern.append(row)
        if row == 0:
            direction = 1
        elif row == key-1:
            direction = -1
        row += direction

    counts = [pattern.count(i) for i in range(key)]
    rails = []
    pos = 0

    for count in counts:
        rails.append(list(cipher[pos:pos+count]))
        pos += count

    result = ""
    for r in pattern:
        result += rails[r].pop(0)

    return result

text = input("Enter plaintext: ")
key = int(input("Enter number of rails: "))

cipher = encrypt(text, key)
print("Encrypted:", cipher)
print("Decrypted:", decrypt(cipher, key))

'''
'''
#-------------------------------------col trans
def encrypt(text, key):
    n = len(key)
    text = text.replace(" ", "")

    while len(text) % n:
        text += 'X'

    rows = [text[i:i+n] for i in range(0, len(text), n)]

    result = ""
    for c in sorted(range(n), key=lambda i: key[i]):
        for row in rows:
            result += row[c]

    return result

def decrypt(cipher, key):
    n = len(key)
    rows = len(cipher) // n
    grid = [[''] * n for _ in range(rows)]

    pos = 0
    for c in sorted(range(n), key=lambda i: key[i]):
        for r in range(rows):
            grid[r][c] = cipher[pos]
            pos += 1

    return ''.join(''.join(row) for row in grid)

text = input("Enter plaintext: ")
key = list(map(int, input("Enter key: ").split()))

cipher = encrypt(text, key)
print("Encrypted:", cipher)
print("Decrypted:", decrypt(cipher, key))

'''
'''
#--------------------------------row
text = input("Enter plaintext: ").replace(" ", "")
key = list(map(int, input("Enter key (e.g. 3 1 2): ").split()))

n = len(key)

while len(text) % n != 0:
    text += 'X'

rows = [text[i:i+n] for i in range(0, len(text), n)]

order = sorted(range(n), key=lambda i: key[i])

enc = ""
for row in rows:
    for i in order:
        enc += row[i]

print("Encrypted:", enc)

# Decryption
dec = ""
pos = 0

grid = [[''] * n for _ in rows]

for row in range(len(rows)):
    for col in order:
        grid[row][col] = enc[pos]
        pos += 1

for row in grid:
    dec += ''.join(row)

print("Decrypted:", dec)
'''
'''
#---------------------------------------------------------des
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = b'12345678'

text = input("Enter plaintext: ").encode()

cipher = DES.new(key, DES.MODE_ECB)

enc = cipher.encrypt(pad(text, 8))
print("Encrypted:", enc.hex())

dec = unpad(cipher.decrypt(enc), 8)
print("Decrypted:", dec.decode())
'''
'''
#-------------------------------------------------------aes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'1234567890123456'

text = input("Enter plaintext: ").encode()

cipher = AES.new(key, AES.MODE_ECB)

enc = cipher.encrypt(pad(text, 16))
print("Encrypted:", enc.hex())

dec = unpad(cipher.decrypt(enc), 16)
print("Decrypted:", dec.decode())
'''
'''
#------------------------------------------rsa
p = 61
q = 53

n = p * q
phi = (p-1) * (q-1)

e = 17
d = pow(e, -1, phi)

print("Public key:", e, n)
print("Private key:", d, n)

text = input("Enter plaintext: ")

enc = ''
al_enc=''
for ch in text:
    enc+=chr(pow(ord(ch), e, n))
    al_enc+=chr(pow(ord(ch), e, n)%26+65)

print("Encrypted:", al_enc)

dec = ""
for ch in enc:
    dec += chr(pow(ord(ch), d, n))

print("Decrypted:", dec)
'''
