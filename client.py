import socket
import sys
import os
import datetime
import hashlib

def shortlist(socket1):
	while 1:
		data = socket1.recv(1024).decode()
		if data.endswith('||end||'):
			print data[:-7]
			break
		print data

def longlist(socket1):
	while 1:
		data = socket1.recv(1024).decode()
		if data.endswith('||end||'):
			print data[:-7]
			break
		print data

def Filehashsingle(socket1):
	data = socket1.recv(1024).decode()
	print data

def Filehashmultiple(socket1):
	while 1:
		data = socket1.recv(1024).decode()
		if data.endswith('||end||'):
			print data[:-7]
			break
		print data

def downloadFile(s,file1,message):
	flag = 0
	with open(file1, 'wb') as f:
		s.send(message.encode())
		while 1:
			data = s.recv(1024)
			if (data.decode() == 'Error: File Not Found!'):
				print('Error opening file or file does not exist')
				flag = 1
				break
			f.write(data)
			if len(data) < 1024:
				print 'File downloaded'
				break
	f.close()
	if (flag == 0):
		data = s.recv(1024).decode()
		print data
	else:
		pass

def downloadFile_udp(s,file1,host,port_udp,message):
	flag = 0
	udp_soc=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_soc.bind((host, port_udp))
	f = open(file1, 'wb')
	s.send(message.encode())
	try:
		while(True):
			data, addr=udp_soc.recvfrom(1024)
			if (data == 'Error: File Not Found!'):
				print('Error opening file or file does not exist')
				flag = 1
				break
			udp_soc.settimeout(2)
			f.write(data)
	except socket.timeout:
		f.close()
		udp_soc.close()
	f.close()
	if (flag == 0):
		data = s.recv(1024).decode()
		print data
		print 'File Downloaded'
	else:
		f.close()
		udp_soc.close()
	

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print "Socket object created successfully"
port_udp = 12347
port=8080
host=socket.gethostname()
s.connect((host, port))

while True:
	try:
		data = s.recv(1024).decode()
		print(data)
		message = raw_input("--> ")

		while True:
			msg = message.strip().split(' ')

			if (msg[0] == 'IndexGet'):
				if msg[1]=='shortlist':
					if ((len(msg) == 6) or len(msg) == 7):
						s.send(message.encode())
						shortlist(s)
					else:
						print('Please use appropriate flags')
				elif ((msg[1]=='longlist') and (len(msg)<=3)):
					if ((len(msg)==2) or(len(msg)==3 and msg[2]== '*.txt')) :
						s.send(message.encode())
						longlist(s)
					else:
						print('Please use appropriate flag')
					
				else:
					print('Please use appropriate flag')
			elif msg[0]=='FileHash':
				s.send(message.encode())
				if (msg[1]=='verify' and len(msg) == 3):
					Filehashsingle(s)
				elif (msg[1]=='checkall' and len(msg) == 2):
					Filehashmultiple(s)
				else:
					print("Please use appropriate flags")
			elif msg[0] == 'FileDownload':
				if (len(msg) == 4):
					path = msg[3]
				else:
					addr = msg[1].split('/')
					path = addr[-1]
				if (len(msg) == 2):
					downloadFile(s,path,message)
				elif (msg[2]=='TCP'):
					downloadFile(s,path,message)
				elif (msg[2]=='UDP'):
					downloadFile_udp(s,path,host,port_udp,message)
				else:
					print("Please use appropriate flags")
			elif msg[0] == 'exit':
				s.send(message.encode())
				s.close()
				sys.exit()
			else:
				print 'Invalid Command'
			message = raw_input("--> ")
	except KeyboardInterrupt:
		print 'Socket Closed'
		s.close()
		sys.exit()
	except IndexError:
		print 'Invalid Command'
		continue
	except IOError:
		print 'Wrong File Path'
		continue
'''
To download File : FileDownload pathofFileServer pathofFileClient TCP/UDP
'''