
#!/usr/bin/python
# Borja Egea Madrid

import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind(('localhost', 8080))

# Queue a maximum of 5 TCP connection requests
mySocket.listen(5)

primer = None

while True:
	print 'Waiting for connections'
	(recvSocket, address) = mySocket.accept()
	print 'HTTP request received:'
	peticion = recvSocket.recv(1024)
	num = peticion.split()[1][1:]

	if primer == None:
		primer = num
		recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
				"<html><body><h1>Dame otro numero </h1></body></html>" +
				"\r\n")
	
	else:
		try:
			suma = int(primer) + int(num)	
			recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
					"<html><body><h1>" + str(primer) + " + " + str(num) + " = " + str(suma) + "</h1></body></html>"
					+ "\r\n")
	
			primer = None			

		except ValueError:
			recvSocket.send("HTTP/1.1 400 Error..\r\n\r\n" +
					"<html><body><h1>No podemos sumar enteros y caracteres</h1></body></html>"
					+"\r\n")

			primer = None
	recvSocket.close()
	
