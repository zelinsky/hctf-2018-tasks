

def create_char(cur, want):
    return cur ^ want

def flip_char(pos, want):
    return create_char(msg[pos], want)


hex_i = "e85e8b5dd166139119609572a47b9e2dae7c0427bb3d9e566a517f9ab9a953ad9dd7be1d42a0846245b7ac071f69dc446f1afb1fc9296114adf258a411a1d6e52b425bd61ad3446ec80af8003e4eac0cd6951b44d13f10b06c6271380e828cb8937bda48f8ef09376151f6d97ce4f4c2da47193de62446ee1347c0a379d87f425c8332604567e9c0faa334463a42297a67dd9b2fc695f10ec03c13eb715d0502eb697f8076e220b3955a18831c5f903dadb68c010181673fa74bdab67f9351ef3546e4a43ddf4df7dfd007de9ef5da12230199ac3a374202bb99e98967248e856eda0990b3c264377139856504b54c5061c8698ec54c93a4683ba721ba0efc4de04868d1ebc3feab253c6042d4f6c1f4e19028a8de4e83b68c3a8564b2cec6b3"
c = bytes.fromhex(hex_i)
msg =  b'{"f": "markdown", "c": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "t": "html4"}'
new = bytearray(c)

wanted = b'"|cat f* #"' # b'"html << #   "' # b'"a|ls #   "'

for i in range(5, len(wanted) + 5):
    new[i] = c[i] ^ msg[i] ^ wanted[i-5]

print(new.hex())