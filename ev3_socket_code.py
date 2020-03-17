#!/usr/bin/env python3
#EV3 Code
#Starts a listening server, echoes what is received!

import sys
import socket
import time

#Function for a testing environment; id should be hardcoded.
def get_id():
	id = 0
	while id not in [1, 2, 3]:
		id = int(input("Which ev3 is this? (1, 2, 3): "))
	return id

#Create a TCP/IP socket.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind that socket to an address, and start listening for connections
while True:
	try:
		id = get_id()
		#reiterating - this should be hardcoded in final imp.
		DEFAULT_ADDR = ('localhost', 10000 + id)
		server_addr = DEFAULT_ADDR

		print("Attempting to start up listening server on %s port %s" % server_addr)
		server_socket.bind(server_addr)
		print("Server bound successfully.")
		break
	except:
		print("That address is in use")

server_socket.listen(5)
conn_socket, pi_addr = server_socket.accept()
print("New connection from: ", pi_addr)

def send_message(socket, message):
	print("Sending message ", message, " to socket ", socket.getsockname())
	socket.send(message.encode())

def parse_command(command):
	print("Command", command, "is not yet implemented, but would at this point involve moving some motors!")

#Wait for a message, parse it using the above command parser, then send back an acknowledgement.
while True:
	try:
		data = conn_socket.recv(1024)
	except KeyboardInterrupt:
		print("Caught keyboard interrupt, closing current sockets and exiting")
		conn_socket.close()
		server_socket.close()
		sys.exit(1)
	if data:
		#we've got a message!
		command = data.decode()
		print("Received ", command, " from ", conn_socket.getpeername())
		response = "ACK: " + command
		parse_command(command)
		send_message(conn_socket, response)
	else:
		#connection closed by client, close our sockets.
		print("Connection closed by pi, shutting down.")
		conn_socket.close()
		server_socket.close()
		sys.exit(1)
