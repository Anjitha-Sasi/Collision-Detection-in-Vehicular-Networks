import socket
from threading import Thread
from collections import namedtuple
from bitarray import bitarray


class frame:
	def __init__(self):
		self.frame_data = namedtuple("MyFrame", "SOF ID RTR IDE R0 DLC DATA CRC ACK EOF IFS")
		self.frame_remote = namedtuple("frame_remote","SOF ID RTR IDE R0 DLC CRC ACK EOF IFS")
		self.frame_error = namedtuple("frame_error","DATA FLAG DEL OVERLOAD")
		self.frame_overload = namedtuple("frane_overload","FLAG ACTIVE DEL")
	def dataframe(self):
		SOF=bitarray(7)
		ID=bitarray(11)
		RTR=bitarray(1)
		IDE=bitarray(1)
		R0=bitarray(1)
		DLC=bitarray(4)
		DATA=bitarray(64)
		CRC=bitarray(16)
		ACK=bitarray(2)
		EOF=bitarray(7)
		IFS=bitarray(7)
		return(SOF+ID+RTR+IDE+R0+DLC+DATA+CRC+ACK+EOF+IFS)
	def remoteframe(self):
		SOF=bitarray(7)
		ID=bitarray(11)
		RTR=bitarray(1)
		IDE=bitarray(1)
		R0=bitarray(1)
		DLC=bitarray(0)
		CRC=bitarray(16)
		ACK=bitarray(2)
		EOF=bitarray(7)
		IFS=bitarray(7)
		return(SOF+ID+RTR+IDE+R0+DLC+CRC+ACK+EOF+IFS)
	def errorframe(self):
		DATA=bitarray(64)
		FLAG=bitarray(12)
		DEL=bitarray(8)
		OVERLOAD=bitarray(20)
		return(DATA+FLAG+DEL+OVERLOAD)
	def overloadframe(self):
		FLAG=bitarray(12)
		ACTIVE=bitarray(6)
		DEL=bitarray(8)
		return(FLAG+ACTIVE+DEL)

import socket
from threading import Thread

sock=socket.socket()
port=12345
sock.bind(('',port))
sock.listen(5)
c,addr=sock.accept()

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def sendd():
	print(addr)
	while True:
		a=input('message:')
		c.send(a)
		if a=='close':
			break

	c.close()
	sock.close()

def received():
	while True:
		message=c.recv(1024)
		message = str(message)
		s = "".join(format(ord(x), 'b') for x in message)
		print("client :",s)
		if message=='close':
			print("Client disconnected")
			break


t1=Thread(target=sendd)
t2=Thread(target=received)


t1.start()
t2.start()

t1.join()
t2.join()
