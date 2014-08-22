#!/usr/bin/python

import smtplib, logging, string

# This is for logging any exceptions and/or errors. It will be logged in /var/log/syslog with message similar to
# '2014-08-18 16:24:58,064 ERROR service_start global name 'sendeail' is not defined'
logging.basicConfig(filename='/var/log/syslog', format='%(asctime)s %(levelname)s %(funcName)s %(message)s', level=logging.ERROR)

# This function is used for sending authenticated email. 
def sendemail(status,To, From, Server, port, username, password, bodymessage):
	try:	
		SUBJECT = status
		TO = To
		FROM = From
		text = bodymessage
		BODY = string.join(( "From: %s" % FROM, "To: %s" % TO, "Subject: %s" % SUBJECT , "", text), "\r\n")
		server = smtplib.SMTP()
		server.connect(Server, port)
		server.starttls()
		server.login(username, password) 		
		server.sendmail(FROM, [TO], BODY)
		server.quit()
	except Exception, e:
		logging.error(e)
		
def main():
	sendemail(status,To, From, Server, port, username, password, bodymessage)		

if __name__ == '__main__':
	main()
