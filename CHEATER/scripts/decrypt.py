from Crypto.Cipher import AES
from base64 import b64decode
key = b"#\x9dc\xf6\x91w\xb4\xb4\xfe\x99`d\xf3\x85\xd5\xb2"

aes = AES.new(key, AES.MODE_ECB)

print(aes.decrypt(b64decode("LTIyOT/9e+HWAeHeVLD7nTrKWNTRB31Oxi1OyRF7w/axi/DvePbBvOBggxt5QeCvxAlUUQZ/zm+Wk7rXVwXhebEukOaFYQlq9MrM58IxpQ6wj6bvKAtKTdJWFYoho1f3")))