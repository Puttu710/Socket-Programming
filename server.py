import socket
import os
import sys
import datetime
import time
import hashlib

def shortlist(c,date1,time1,date2,time2):
	date11 = tuple(map(int,date1.split('-')))
	time11 = tuple(map(int,time1.split(':')))
	date22 = tuple(map(int,date2.split('-')))
	time22 = tuple(map(int,time2.split(':')))
	strtime = datetime.datetime(date11[0],date11[1],date11[2],time11[0],time11[1],time11[2])
	endtime = datetime.datetime(date22[0],date22[1],date22[2],time22[0],time22[1],time22[2])
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	if len(files)==0:
		ans = "No files in current directory"
		c.send(ans.encode())
		print ans
	else:
		for f in files:
			ftime = datetime.datetime.fromtimestamp(os.path.getmtime(f))
			name, ext = os.path.splitext(f)
			if ftime>strtime and ftime<endtime:
				ans = "Name: " + f + "   Size: " + str(os.path.getsize(f)) + "   Timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   Extension: " + ext
				c.send(ans.encode())
				print ans
	rem = '||end||';
	c.send(rem.encode())
	if len(files)!=0:
		print 'Sent details successfully'

#### BONUS #####
def shortlist_specific(c,date1,time1,date2,time2,type1):
	date11 = tuple(map(int,date1.split('-')))
	time11 = tuple(map(int,time1.split(':')))
	date22 = tuple(map(int,date2.split('-')))
	time22 = tuple(map(int,time2.split(':')))
	strtime = datetime.datetime(date11[0],date11[1],date11[2],time11[0],time11[1],time11[2])
	endtime = datetime.datetime(date22[0],date22[1],date22[2],time22[0],time22[1],time22[2])
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	n = 0
	type1 = type1[1:5]
	for f in files:
		ftime = datetime.datetime.fromtimestamp(os.path.getmtime(f))
		name, ext = os.path.splitext(f)
		if ftime>strtime and ftime<endtime and ext==type1:
			ans = "Name: " + f + "   Size: " + str(os.path.getsize(f)) + "   Timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   Extension: " + ext
			c.send(ans.encode())
			print ans
			n = n+1
	if n!=0:
		print 'Sent details successfully'
	else:
		ans = "No files of given extension in current directory"
		c.send(ans.encode())
		print ans
	rem = "||end||"
	c.send(rem.encode())

def longlist(c):
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	if len(files)==0:
		ans = "No files in current directory"
		c.send(ans.encode())
		print ans
	else:
		for f in files:
			ftime = datetime.datetime.fromtimestamp(os.path.getmtime(f))
			name, ext = os.path.splitext(f)
			ans = "Name: " + f + "   Size: " + str(os.path.getsize(f)) + "   Timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   Extension: " + ext
			c.send(ans.encode())
			print ans
	rem = '||end||';
	c.send(rem.encode())
	if len(files)!=0:
		print 'Sent details successfully'

###### BONUS #####
def longlist_specific(c):
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	n = 0;
	for f in files:
		ftime = datetime.datetime.fromtimestamp(os.path.getmtime(f))
		name, ext = os.path.splitext(f)
		flag = 0
		if ext == '.txt':
			term = "programmer"
			file = open(f)
			for line in file:
				line = line.strip().split(' ')
				if term in line:
					flag = 1
					break;
			file.close()
		if flag==1:
			ans = "Name: " + f + "   Size: " + str(os.path.getsize(f)) + "   Timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   Extension: " + ext
			c.send(ans.encode())
			print ans
			n = n+1
	if n!=0:
		print 'Sent detail successfully'
	else:
		ans = "No text files containing word programmer"
		c.send(ans.encode())
		print ans
	rem = '||end||';
	c.send(rem.encode())

def Filehashsingle(c,file):
	hash_md5 = hashlib.md5()
	try:
		with open(file, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		ans = "Hash: " + hash_md5.hexdigest()+ "   Last Modified: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
		c.send(ans.encode())
		print("Hash sent for the file " + str(file))
	except:
		ans = "Requested file does not exist."
		print ans
		c.send(ans.encode())

def Filehashmultiple(c):
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	for file in files:
		hash_md5 = hashlib.md5()
		with open(file, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		ans = "File Name: "+file +"   Hash: " + hash_md5.hexdigest() + "   Last Modified: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
		c.send(ans.encode())
	rem = '||end||'
	c.send(rem.encode())
	print("Hash sent for all the files.")

def sendFile(c,file):
	try:
		f = open(file,'rb')
		l = f.read(1024)
		while (l):
			c.send(l)
			l = f.read(1024)
		print str(file) + ' sent through TCP.'
		f.close()
		hash_md5 = hashlib.md5()
		with open(file, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		ans = "File Name: " + file + "   Size: " + str(os.path.getsize(file)) + "   Timestamp: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S') + "   Hash: " + hash_md5.hexdigest()
		c.send(ans.encode())
	except:
		print('Error opening file or file does not exist')
		c.send('Error: File Not Found!'.encode())
	

def sendFile_udp(c,file,port_udp,host):
	udp_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dest = (host, port_udp)
	try:
		f=open(file,'rb')
		l=f.read(1024)
		while(l):
			if(udp_soc.sendto(l,dest)):
				l = f.read(1024)
		udp_soc.close()
		f.close()
		print str(file) + ' sent through UDP.'
		hash_md5 = hashlib.md5()
		with open(file, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		ans = "File name: " + file + "   Size: " + str(os.path.getsize(file)) + "   Timestamp: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S') + "   hash: " + hash_md5.hexdigest()
		c.send(ans.encode())
	except:
		print('Error opening file or file does not exist')
		udp_soc.sendto('Error: File Not Found!',dest)
	

if __name__ == "__main__" :

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print "Socket successfully created"
	
	port = 8080
	port_udp = 12347
	host = socket.gethostname()
	s.bind((host, port))
	s.listen(5)
	while True:
		try:
			c,addr=s.accept()
			s.settimeout(.5)
			print("Connection received from: " + str(addr))
			currentTime = time.ctime(time.time()) + "\r\n"
			c.send(currentTime.encode('ascii'))
			c.send('Thank you for connecting')

			while True:
				val = c.recv(1024).decode()
				vald = val.strip().split(' ')
				### IndexGet
				if (vald[0] == "IndexGet" and len(vald)>=2):
					if (vald[1] == "shortlist"):
						if (len(vald) == 6):
							shortlist(c,vald[2],vald[3],vald[4],vald[5])
						else:
							shortlist_specific(c,vald[2],vald[3],vald[4],vald[5],vald[6])	
					elif (vald[1] == "longlist"):
						if (len(vald) == 2):
							longlist(c)
						elif (len(vald) == 3):
								longlist_specific(c)

				### FileHash
				elif (vald[0] == "FileHash" and len(vald)>=2):
					if (vald[1] == "verify" and len(vald)==3):
						Filehashsingle(c,vald[2])
					elif (vald[1] == "checkall"):
						Filehashmultiple(c)

				### FileDownload
				elif (vald[0] == "FileDownload"):
					if (len(vald) == 2):
						sendFile(c,vald[1])
					elif (vald[2] == "TCP"):
						sendFile(c,vald[1])
					elif (vald[2] == "UDP"):
						sendFile_udp(c,vald[1],port_udp,host)
				elif (vald[0] == 'exit'):
					print('Client aborted connection')
				else:
					print("Invalid Command")
					break

		except KeyboardInterrupt:
			print 'Socket Closed'
			s.close()
			sys.exit()
		except socket.timeout:
			print 'Client Disconnected'
			s.settimeout(None)
		c.close()
	s.close()