#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket
import ssl
import sys
import random
import string
import struct
import binascii

class Client(object):
    def __init__(self, nick, host="dev1.froger.p2.tiktalik.com", port=9900):
        self.nickname = nick
        self.host = host
        self.port = port
        self.session_id = None
        self.session_private_vector = []
        self.ssl_sock = None

        self.__connect_server(self.host, self.port)
        self.__handshake()

    def __connect_server(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(s)
        ssl_sock.connect((host, port))
        self.ssl_sock = ssl_sock

    def __ssl_write(self, msg):
        print "sending msg..."
        print self.ssl_sock.write(msg)
        print "message sent"

    def __ssl_read(self):
        return self.ssl_sock.read()
    
    def __handshake(self):
        """
        handshake command:
        [pkg_len(4bytes)][command_len(2bytes)][command][nickname_len(2bytes)][nickname]
        """
        cmd = "create_session"
        cmd_len = len(cmd)
        nick_len = len(self.nickname)
        
        fmt = "!i H %ds H %ds" % (cmd_len, nick_len)
        pkg_len = 4 + 2 + cmd_len + 2 + nick_len
        s = struct.Struct(fmt)
        pkg = s.pack(pkg_len, cmd_len, cmd, nick_len, self.nickname)

        print "pkg_len = %d" % pkg_len
        self.__ssl_write(pkg)
        print "answer %r: " % self.__ssl_read()

    def set_session_id(self, ssid):
        self.session_id = ssid

    def generate_private_session(self, nickname):
        chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
        rand_text = ''.join(random.choice(chars) for x in range(10))
        return {nickname: rand_text}

def main(argv):
    """
    froger88: Simle Python Client, not really functional - for now, used
        just for server debug and Test-Driven-Development
        (in that case Client-Driven-Development ;) )
    """
    
    host="dev1.froger.p2.tiktalik.com"
    port=9900

    nickname = raw_input("Enter nickname: ")
    
    me = Client(nickname, host, port)
    
    while True:
        message = raw_input("Enter message: ")
        me.write_message(message)
        
        data = ssl_sock.read()
        print "server response: ", data
        print "private_session(data) = %s" % me.generate_private_session(data)

        if data.startswith("quit"):
            break

    ssl_sock.close()

if __name__ == "__main__":
    main(sys.argv)
