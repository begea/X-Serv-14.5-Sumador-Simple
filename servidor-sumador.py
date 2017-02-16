#!/usr/bin/python3

import socket
import random

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind(('localhost', 8081))

# Queue a maximum of 5 TCP connection requests
mySocket.listen(5)

primer = None
try:
	while True:
		print ('Waiting for connections')
		(recvSocket, address) = mySocket.accept()
		print ('HTTP request received:')
		peticion = recvSocket.recv(2048).decode('utf-8')
		num = peticion.split()[1][1:]

		if primer == None:
			primer = num
			recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
				"<html><body><h1>Primer numero: " + str(primer) + ". Dame otro número.""</h1></body></html>"
					+ "\r\n", 'utf-8'))

		else:
				try:
					suma = int(primer) + int(num)

					recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
						"<html><body><h1>" + str(primer) + " + " + str(num) + " = " + str(suma) + "</h1></body></html>"
							+ "\r\n", 'utf-8'))

					primer = None

				except ValueError:
					recvSocket.send(bytes("HTTP/1.1 400 Error..\r\n\r\n" +
						"<html><body><h1>No podemos sumar enteros y caracteres</h1></body></html>"
							+ "\r\n", 'utf-8'))

					primer = None
	recvSocket.close()

except KeyboardInterrupt:
	print ("Closing binded socket")
	mySocket.close()
	
