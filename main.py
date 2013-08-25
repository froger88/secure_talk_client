#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket, ssl, sys

def main(argv):
    """
    froger88: Simle Python Client, not really functional - for now, used
        just for server debug and Test-Driven-Development
        (in that case Client-Driven-Development ;) )
    """

    HOST = "127.0.0.1"
    PORT = 9900
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # require a certificate from the server
    ssl_sock = ssl.wrap_socket(s)

    ssl_sock.connect((HOST, PORT))

    while True:
        message = raw_input("Enter message: ")
        ssl_sock.write(message)
        
        data = ssl_sock.read()
        print "server response: ", data

        if data.startswith("quit"):
            break

    ssl_sock.close()

if __name__ == "__main__":
    main(sys.argv)
