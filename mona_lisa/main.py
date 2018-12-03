from helpers import image_helper

flag = 'FLAG{THIS-IS-THE-WATER-AND-THIS-IS-THE-WELL-§$%&/}'
path_orig = 'mona_lisa.png'
path_stego = 'mona_lisa_stego.png'

image_helper.encode(flag, path_orig, path_stego)
decode = image_helper.decode(path_orig, path_stego)

print(decode)
