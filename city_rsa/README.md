Converter
=========

## Description
Chal comes with a services that signes messages with an unknown RSA private key.
One must create a signature for the message "YES, I did eat that cookie". The word "YES" is filtered though...

One has to use a buffer overflow to create an error in the RSA CRT calculation to leak the private key.

## CTF Description

I know that frank that a\*\*hole ate the last cookie, but no one believes me.

He wrote himself a service to sign messages, I found it here:

```
nc play.wass-ctf.xyz 4422
```

Can you get me the message "YES, I did eat the last cookie" signed by his service?

I added a verifier for you using his public key:

```
nc play.wass-ctf.xyz 31337
```

## Infos

* Author: rg
* Ports: 4422, 31337
* Category: cry
* For Downloading: main.c, main.py
* Flag: flag{https://www.youtube.com/watch?v=MpMBETNC-44#C0ngr4tz}
* Points: 300
