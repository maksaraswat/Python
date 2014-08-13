#!/usr/bin/python

import datetime, paramiko, os, zipfile

#Formatting Date and Creating Directory
today=datetime.date.today()-datetime.timedelta(days=3)
formattedtime = today.strftime('%Y%m%d')	
destination = '~/TestDir-%s'%formattedtime
if not os.path.exists(destination):
	os.mkdir(destination)

# This function downloads the file using Paramiko
# and saves in specfied directory

def file_download(hostname, username,port, password):
#	mykey = paramiko.RSAKey.from_private_key_file('~/My-ssh.priv')  # This is when password less login is setup
	password = password                                             # This is used when password is used to login  	
	host = hostname
	username = username
	port = port
	transport = paramiko.Transport((host, port))
#	transport.connect(username = username, pkey = mykey) 		# This is when password less login is setup
	transport.connect(username = username, password = password)	# This is used when password is used to login
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.chdir('outgoing')
	for filename in sftp.listdir():
		try:
			if filename.startswith('file_%s.csv'%formattedtime):
				localpath= destination + '/' + filename
				print "Downloading files ==> " + filename
				sftp.get(filename, localpath)	
		except IOError as e:
			print e
	sftp.close()
	transport.close()

# This function calls the file_download function 
# and moves the files to required directory. If 
# using shutil.move() then it copies permissions 
# also which is not desirable always. 

def main():
	try:	
		file_download('www.blah.com', 'neo', 22, 'ilovematrix')
		currentfile = os.getcwd() + '/' + 'file_%s.csv'%formattedtime 	
		shutil.copy(currentfile, destination)	
		os.remove(currentfile)
	except Exception as e:
		print e

if __name__ == '__main__':
	main()
