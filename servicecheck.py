#!/usr/bin/python

# This program checks the status of service(s) 
# running, tries to restart them and send out email(s)
# if fails to start service or there is any error(s).

import time, subprocess, smtplib, string, logging, commands

# This is for logging any exceptions and/or errors.
# It will be logged in /var/log/syslog with message similar to
# '2014-08-18 16:24:58,064 ERROR service_start global name 'sendeail' is not defined'
logging.basicConfig(filename='/var/log/syslog', format='%(asctime)s %(levelname)s %(funcName)s %(message)s', level=logging.ERROR)

# This function is used for sending authenticated
# email with status and/or error/exception
def sendemail(status):
	try:	
		SUBJECT = 'Service ' + status
		TO = "email@gmail.com"
		FROM = "email@gmail.com"
		text = status
		BODY = string.join(( "From: %s" % FROM, "To: %s" % TO, "Subject: %s" % SUBJECT , "", text), "\r\n")
		server = smtplib.SMTP()
		server.connect('smtp.gmail.com', 587)
		server.starttls()
		server.login('gmailusername', 'gmailpassword') 		
		server.sendmail(FROM, [TO], BODY)
		server.quit()
	except Exception, e:
		logging.error(e)

# This function restarts service and calls
# sendemail(status) function to send email
# with status and/or exceptions.
def service_start(servicename):
	try:
		start_service = subprocess.call(['start', servicename])
		if start_service == 0:
			sendemail(servicename + ' Started Successfully.')
		else:
			sendemail(servicename + ' start FAILED.')
	except Exception, e:
		logging.error(e)

# This is the function where you specify 
# services that needs to be restarted. 
# Based on status of service, it calls 
# service_start(servicename) function.
	
def main():
	try:	
		services = ['vsftpd', 'ssh']
		for service in services:
			try:
				status_service = subprocess.Popen(["status", service], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				out, err = status_service.communicate()
				if "start/running" not in out:
					service_start(service)
			except Exception, e:
				logging.error(e)	
	except Exception, e:
		logging.error(e)	

if __name__ == '__main__':
	main()
