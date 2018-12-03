import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class DH:
    modulus = 0xA503F7833E4D480DE0AC0A4EE332D6EA39B32993B05BC35C10E2ADAA83DBC50287720AFBB5D621ED53B2583A8859DCE2710EBD266173FB9F58A2B9176B4DAC6992DE8FE8C12223C95F202C793C775E611B0E2B3EEE845CC7437CB58584D4874162B25AA511DDD57F6D7E966DEBA502A92AAAF941ED697373E79218999055B3AF
    generator = 2

    def __init__(self):
        self.priv_exp = 79229988863589352108904174294629155634383636854832161146796627546338854940885908052562044914172726605454490116912987540062759497203041123022582825013272037877964629441787462115781406325154912095939196259905724348681122335819986259406215859599165320625548682546933693659335249383848047548628819054807
        self.pub_num = pow(self.generator, self.priv_exp, self.modulus)

    def calc_shared_key(self, peer_num):
        return pow(peer_num, self.priv_exp, self.modulus)

    def calc_aes_key(self, peer_num):
        shared_secret = self.calc_shared_key(peer_num)
        return shared_secret.to_bytes(128, "big")[:16]


class AesCipher:

    def __init__(self, key):
        backend = default_backend()
        self.cipher = Cipher(algorithms.AES(key), modes.ECB(), backend)
        self.padder = padding.PKCS7(len(key) * 8)

    def encrypt_b64(self, msg):
        ct = self.encrypt(msg)
        return base64.b64encode(ct)

    def decrypt_b64(self, ct):
        ct = base64.b64decode(ct)
        return self.decrypt(ct)

    def pad(self, msg):
        padder = self.padder.padder()
        return padder.update(msg) + padder.finalize()

    def unpad(self, msg):
        unpadder = self.padder.unpadder()
        return unpadder.update(msg) + unpadder.finalize()

    def encrypt(self, msg):
        encryptor = self.cipher.encryptor()
        padded = self.pad(msg)
        return encryptor.update(padded) + encryptor.finalize()

    def decrypt(self, ct):
        decryptor = self.cipher.decryptor()
        msg = decryptor.update(ct) + decryptor.finalize()
        return self.unpad(msg)
