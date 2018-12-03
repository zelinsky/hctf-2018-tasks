Seccompstuff
=========

## Description
Seccomp filter does not take x86 syscall nrs into account.
Open file by switching into 32bit mode.

## CTF Description

It's seccomp so it's secure.

```
nc play.wass-ctf.xyz 13376
```

## Infos

* Author: kw
* Ports: 13376
* Category: pwn
* For Downloading: seccomp seccomp.c
* Flag: flag{e5eb5ea8b23cc29ed78166b67a2c70b00}
* Points: 250
