from PIL import Image
from lcg import LCG


def create_image_pw(path, user_id):
    l = LCG(user_id)
    buf = b""

    for _ in range(128):
        buf += l.next().to_bytes(16, "big")


    im = Image.frombytes("1", (128, 128), buf)
    im.save(joinp(path, "{}.bmp".format(user_id)))
    return l.next()
