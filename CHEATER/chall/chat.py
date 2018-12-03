#!/usr/bin/env python3
import socket
from sys import argv

from crypto import DH, AesCipher

peers = {}


def int_to_str(val):
    return str(val).encode()


def str_to_int(num):
    return int(num.decode())


def pack_msg(msg):
    pkg_len = len(msg) + 5
    # prepend length as 4 byte ascii num
    len_str = "{:04},".format(pkg_len)
    return len_str.encode() + msg


def unpack_msg(msg):
    # Skip length and comma
    return msg[5:]


class Peer:

    def __init__(self, ip, port, dh):
        self.dh = dh
        self.ip = ip
        self.port = port
        self.cipher = None

    def set_key(self, dh_pub):
        self.cipher = AesCipher(self.dh.calc_aes_key(dh_pub))

    def decrypt(self, ct):
        return self.cipher.decrypt_b64(ct)

    def encrypt(self, msg):
        return self.cipher.encrypt_b64(msg)


class Sender:

    def __init__(self, peer_ip, peer_port=1234, recv_port=1337):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", recv_port))
        self.sock.settimeout(1)
        self.peer = Peer(peer_ip, peer_port, DH())
        self.shake_hands()

    def send_to_peer(self, msg):
        msg = pack_msg(msg)
        self.sock.sendto(msg, (self.peer.ip, self.peer.port))

    def recv(self):
        msg_len = int(self.sock.recv(4, socket.MSG_PEEK))
        return unpack_msg(self.sock.recv(msg_len))

    def shake_hands(self):
        # Send our public number
        self.send_to_peer(int_to_str(self.peer.dh.pub_num))
        # Receive peers public number
        pub_num = self.recv()
        self.peer.set_key(str_to_int(pub_num))

    def send_msg(self, msg):
        self.send_to_peer(self.peer.encrypt(msg))


class Receiver:

    def __init__(self, ip="0.0.0.0", port=1234):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.peer = None
        self.shake_hands()

    def recvfrom(self):
        # Get length of message
        msg_len = int(self.sock.recv(4, socket.MSG_PEEK))
        data, addr = self.sock.recvfrom(msg_len)
        return unpack_msg(data), addr

    def shake_hands(self):
        pub_num, peer_adr = self.recvfrom()
        self.peer = Peer(peer_adr[0], peer_adr[1], DH())
        self.peer.set_key(str_to_int(pub_num))
        msg = pack_msg(int_to_str(self.peer.dh.pub_num))
        self.sock.sendto(msg, (self.peer.ip, self.peer.port))

    def loop_and_print(self):
        while True:
            data, _ = self.recvfrom()
            print(self.peer.decrypt(data).decode())


def listen():
    print("Waiting for incoming connection...")
    rec = Receiver()
    print("Connected! Printing incoming messages:")
    rec.loop_and_print()


def send(ip, port):
    print("Trying to connect to peer...")
    snd = Sender(ip, port)
    print("Connected! Type messages to send:")
    while True:
        msg = input("Msg: ")
        snd.send_msg(msg.encode())


if __name__ == '__main__':
    try:
        if argv[1] == "-l":
            listen()
        else:
            send(argv[2], int(argv[3]))
    except IndexError:
        print("Usage for sending: ./chat.py -s [dst_ip] [dst_port]")
        print("Usage for receiving: ./chat.py -l")
