#!/usr/bin/env python3
from math import gcd
from sys import argv, exit

def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

if len(argv) < 2:
    print("Call with cfg name as param.")
    exit(1)

FILE_FORMAT = "0x{p:x},0x{q:x},0x{p_inv:x},0x{d:x},0x{e:x},0x{d_p:x},0x{d_q:x}"

q = 0xb9fd234059b50e374e11fc1ef48ed972fb37f120264ef816bacb458f33724713174aa7bb09311a30919d11e268a47c17f6dc18bfe5601f7c010635b67a0082615f3979e87e5971861088d78c3300e46d3a2bd59b3b3300e519c15ea2c3cbdbdfa060ba89016f1ebe858b95e5c8169d940861ed2a396f630185300e637dd528b5
p = 0xd224fd10951f633fd3e475614e91adbaa5b215b428c6f00c705fbcb4eea38c12c0de84cd7c8db23f0ac12637791b9a41f8a001b40c9835ee0be3c1620928b9fa54c1038c8bbf01d461b33ebccfe31e6127e1deed82e6bf76f5a4aef3022616c850c923d90c01c070f7d1098c2e153b59d72636445ce061592540a2e6715dd767

# Mutliplizieren grosser Primzahlen ist eine Falltuere
N = p * q

phi = (p-1)*(q-1)

e = 65537
assert gcd(e, phi) == 1, 'Phi und e sind nicht teilerfremd!'
assert e < phi, 'e ist zu gross!'
assert e > 0, 'e ist zu klein!'

greatest_cd, x, y = xgcd(e, phi)
d = (x + phi) % phi # falls x negativ

greatest_cd, x, y = xgcd(p, q)
p_inv = (x + q) % q

d_p = d % (p-1)
d_q = d % (q-1)

print("""RSA Parameters:
p = {p:x},
q = {q:x},
N = p * q = {N:x},
phi = (p-1)*(q-1) = {phi:x},
p_inv = {p_inv:x}
e = random var = {e:x},
d = mult. inverse to e = {d:x}.
d_p = needed for CRT = {d_p:x}.
d_q = needed for CRT = {d_q:x}.


Private Key = (N, e)
Public Key = (N, d)
""".format(**locals()))



with open(argv[1], "w") as f:
    f.write(FILE_FORMAT.format(**locals()))

    