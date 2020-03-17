#!/usr/bin/env python3
#PI CODE
#Establishes an individual connection with the ev3s, who each are basically echo servers.


import sys
import socket
import time

retry_delay = 2
DEFAULT_ADDR = ('localhost', 10000)
#These need to be replaced by the ev3 ips
ev3_1_addr = ('localhost', 10000 + 1)
ev3_2_addr = ('localhost', 10000 + 2)
ev3_3_addr = ('localhost', 10000 + 3)

addresses = [ev3_1_addr,ev3_2_addr,ev3_3_addr]

# Create 3 TCP/IP sockets
ev3_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sockets = [ev3_1,ev3_2,ev3_3]

for i in range(3):
	#print("Connecting socket", i)
	socket = sockets[i]
	while True:
		try:
			print("Connecting socket", i, "with address", addresses[i])
			socket.connect(addresses[i])
			print("Socket", i, "connected")
			break
		except KeyboardInterrupt:
			print("Caught keyboard interrupt, closing current sockets and exiting")
			for j in range(i):
				socket = sockets[j]
				socket.close()
				print("Socket", j+1, "closed.")
			sys.exit(1)
		except Exception as e:
			print("Caught exception '%s', retrying in %ss" % (e, retry_delay))
			try:
				time.sleep(retry_delay)
			except KeyboardInterrupt:
				print("Caught keyboard interrupt, closing current sockets and exiting")
				for j in range(i):
					socket = sockets[j]
					socket.close()
					print("Socket", j+1, "closed.")
				sys.exit(1)

#After this point, we should have each of the sockets connected.
#Let's send a test signal, have it echoed.

def send_message(socket, message):
	print("Sending message", message, "to socket", socket.getsockname())
	socket.send(message.encode())

#main loop - user input of command, sends it to each, waits for a response.
while True:
	message = input("Command: ")
	for i in range(3):
		socket = sockets[i]
		send_message(socket, message)
	for socket in sockets:
		response = socket.recv(1024)
		print("Received message", response.decode(), "from socket", socket.getsockname())

#exit and close
for socket in sockets:
	socket.close()
