#!/usr/bin/env python3

import sys
import time
import socket

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>  received: ")
    print(sys.argv)
    sys.exit(1)

HOST, PORT = sys.argv[1:3]
host = HOST
port = int(PORT)
#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        try:
            s.bind((host, port))
            print("Successfully bound to host " + repr(host) + " on port " + repr(port))
            break
        except Exception as e:
            print(e)
            print(host + ":" + str(port) + " Address in use, trying again in 5s")
            time.sleep(5)
    s.listen()
    conn,addr = s.accept()
    with conn:
        print("Connected by", addr)
        #conns = []
        #for i in range(3):
        #    s.listen()
        #    conn, addr = s.accept()
        #    conns.append(conn)
        #    with conn:
        #        print("Connected by", addr)
        #        print(i)
        #return conns
        while True:
            try:
                message = input("Command: ")
                encoded_message = message.encode()
                print("Sending: " + repr(encoded_message))
                conn.sendall(encoded_message)
            except KeyboardInterrupt:
                sys.exit(1)
            except:
                pass

#main stuff
#conn = connect(HOST, PORT)
#while True:
#    command = input("Command: ")
#    send_command(command,conn)
