Slottier machine
=========

## Description
Fastbin tcache attack.
Constrained to a maximum of 7 malloc n bytes / free at pos x / write 8 bytes operations.
Trick 1: Use a seemingly correct memory chunk inside libc's r/w segment to start the fastbin attack.
Trick 2: Overwrite libc base addr reference inside r/w segment (used as an offset by the plt to calculate new function addresses).

## CTF Description

Insert some coins and pop a shell!
(Ty Hack.lu 2018)

```
nc play.wass-ctf.xyz 13371
```

## Infos

* Author: kw
* Ports: 13371
* Category: pwn
* For Downloading: slottiermachine, libc-2.28.so, ld-2.28.so
* Flag: flag{6c2ac0cc1a7b06bab03af4022047b1bd}
* Points: 250
