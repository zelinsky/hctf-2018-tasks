City RSA
===============

## Description
Using the [bellcore attack](https://eprint.iacr.org/2012/553.pdf) the primes and therefore the private key can be reconstructed if an attacker can induce an error during the signing mechanism in RSA-CRT (Chinese-Remainder-Theorem). In this task a error can be induced via a buffer overflow.

## CTF Description
This chinese guy implemented city rsa...

![](https://i.ytimg.com/vi/oekeTYe8Rqw/hqdefault.jpg)

I intercepted the signatur of a secret message, it is:

```
0x75ab1ece23bacdd86c102ae532f5c56bd362b8c820cf02bdaa67974f27f1458b26fa071b7d5d77419ec33d8d96b92e6e1eb9ebd11991e3a3b4be2f1ce936f9dd932647d1566507fd849278e1fe9c3c7821959b0db85e4457caa799a6da4aba010877d5160819638d4b86eaf737c86f99951c07520f40a57b9c9e06009d79e38422db1d7c27ee153a53d14daeaf2082589a1d90569aba7d47b88d722161ddae4f7bc1a460058d9a157fe0ada1e121c089784369eac60b0501beaf559a729f385cea244f768a5cff30619ac5ccfe94909326ec9030a882c8c7d356c60a9f7f5a756ab808751f5d9e0ae0d116773e0da5cfe610aa8a40010c85fb92dfc4e21453c
```

Could you please find out what the message was?

The public key (e, N) is:

```
e = 0x10001
N = 0x98ac865ef6a31313e50fb37853ce96804cb2d864e2a4d14bf7cca85a444a40b453de7c3ae8416e8976cd1cac7f548a43fe8c2eb3d4cfcd3808cf9458c0c87bf4c037d515d22d1299b72e79fcd4a1d1531789cb3013031fb0e28fdfe73f090027b3b3428cacef6dbf7823d5da8d3158101e0c07e707224d451fcbb3114ab85a925bcb7faf9b317bbbddba81285ab93f0ee5f968b258f4675e9d893ec7f0e8379b67527d78fe920ab201cb3a6459d4f3902754b36e3264db7727c6d32e014593c39991f54c7b034d69b986616a39454c85d9e032afa853a6e12fea06472ed3573707da3df9ca7ce8d2c3b820e745da6e3cc523789f858d98645ea042bb54b463d3
```

LINK TO TCP SERVICE HERE


## Infos

* Category: Crypto/PWN
* Ports: ??
* Packages: ??
* Flag: flag{husohusohuso}
* For Downloading: Source Code
* Points: 300

