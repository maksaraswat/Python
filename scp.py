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
def file_download():
	mykey = paramiko.RSAKey.from_private_key_file('~/My-ssh.priv')  # This is when password less login is setup
#	password = '/K,@]Fd5'                                           # This is used when password is used to login  	
	host = 'X.X.X.X'
	username = 'Y'
	port = 22
	transport = paramiko.Transport((host, port))
	transport.connect(username = username, pkey = mykey) 		        # This is when password less login is setup
#	transport.connect(username = username, password = password)	    # This is used when password is used to login
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.chdir('dirname')
	for filename in sftp.listdir():
		try:
			if filename.startswith(formattedtime):
				localpath= destination + '/' + filename
				print "Downloading files ==> " + filename
				sftp.get(filename, localpath)	
		except IOError as e:
			print e
	sftp.close()
	transport.close()

# This function unzips the downloaded file
# and removes original zip file
def main():
	file_download()	
	srcdir = destination + '/'
	for x in [doc for doc in os.listdir(srcdir)]:
		fh = open(srcdir + x, 'rb')
		z =zipfile.ZipFile(fh)
		for name in z.namelist():
			print "Unzipping file(s) ==> " + x			
			z.extract(name, srcdir)
		fh.close()
		os.remove(srcdir + x)

if __name__ == '__main__':
	main()
