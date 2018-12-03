from math import gcd
from binascii import unhexlify
# find multiplicative inverse

def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0


N = 0x98ac865ef6a31313e50fb37853ce96804cb2d864e2a4d14bf7cca85a444a40b453de7c3ae8416e8976cd1cac7f548a43fe8c2eb3d4cfcd3808cf9458c0c87bf4c037d515d22d1299b72e79fcd4a1d1531789cb3013031fb0e28fdfe73f090027b3b3428cacef6dbf7823d5da8d3158101e0c07e707224d451fcbb3114ab85a925bcb7faf9b317bbbddba81285ab93f0ee5f968b258f4675e9d893ec7f0e8379b67527d78fe920ab201cb3a6459d4f3902754b36e3264db7727c6d32e014593c39991f54c7b034d69b986616a39454c85d9e032afa853a6e12fea06472ed3573707da3df9ca7ce8d2c3b820e745da6e3cc523789f858d98645ea042bb54b463d3

e = 0x10001


sig1 = int(open('answ_1.txt').read(), 16)
sig2 = int(open('answ_2.txt').read(), 16)

q = gcd(sig1-sig2, N)
p = N // q


phi = (p-1)*(q-1)

greatest_cd, x, y = xgcd(e, phi)
d = (x + phi) % phi # falls x negativ

print("Found secret d:", hex(d))

msg = int.from_bytes(b"YES, I did eat the last cookie", "big")

enc_msg = pow(msg, d, N)

print("signed msg:", msg, hex(enc_msg))
