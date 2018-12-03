Sandbox compat 2.0
=========

## Description
Seccomp arch is not filtered. Every syscall called from < 4G is killed. It (should) not be possible to escape from < 4G.
Use sysenter instead of int 0x80 to bypass the < 4G constraint.

## CTF Description

description: x86 memory segmentation is easy, just put everything untrusted under 4G. Flag is in "/opt/flag.txt".
(Ty google-ctf 2018)

```
nc play.wass-ctf.xyz 13372
```

## Infos

* Author: kw
* Ports: 13372
* Category: pwn
* For Downloading: src.tar
* Flag: flag{thank_you_for_the_blacklist}
* Points: 300
