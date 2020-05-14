import  string
LETTER = string.ascii_letters
print(LETTER)

msg = 'ABCD'

def gcd(a,b):
    while a!= 0:
        a,b = b%a, a
    return b
def eularPhi(n):
    phi = []
    x =1
    while x<n:
        if gcd(x,n) ==1:
            phi +=[x]  #phi append x.
        x += 1
    return len(phi)

def modinv_(a,m):
    if gcd(a,m) != 1:
        return None
    else:
        return pow(a, eularPhi(m)-1,m)
p =3
k1 =5
k2 =7
c = ((p*k1)+k2)%len(LETTER)
print("Cipher: ",c)
plain = ((c-k2)*modinv_(k1,len(LETTER)))% len(LETTER)
print("PlainText: ", plain)