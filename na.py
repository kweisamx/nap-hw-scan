#!/usr/bin/python
from subprocess import call,check_output
from time import sleep
import urllib2
import smtplib                                                                                                        
from email.mime.text import MIMEText
def send_email():
	msg = "please check your machine right now!!"

	msg = MIMEText(msg)
	msg['Subject'] = 'some has wrong of your server'
	msg['From'] = "sam@nctusam.idv.tw"
	msg['to'] = "kweisaxm0322@gmail.com"
	s = smtplib.SMTP('localhost')
	s.sendmail("sam@nctusam.idv.tw","kweisamx0322@gmail.com",msg.as_string())
	s.quit()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_port(test_port,test_doname,test_name,udp=False):
	try:
		if(udp == False):
			test = check_output(["nc","-zv",test_doname,test_port])
		else:
			test = check_output(["nc","-zvu",test_doname,test_port])
		if not test:# 0 means success
			print(" port %s is open,%s is success "%(test_port,test_name))
		else:
			print("port err")
			send_email()
			raise
	except:
		send_email()
		exit(1)


def check_dns(test,test_name,typeDNS,ip=None):
	test_dns = check_output(["dig","+nocomment","+noadditional","+nostats","+noquestion",test])
	if typeDNS=="CNAME":
		if "nasa.cs.nctu.edu.tw." in test_dns:
			print( "%s is OK, get nasa,cs,nctu.edu.tw\n"%test_name)
		else:
			print("CNAME wrong")
			send_email()
			raise
	elif typeDNS=="A":
		if ip in test_dns:
			print( "%s is OK , NAP2016-DNS2 A record is ip %s "%(test_name,ip))
		else:
			print("A record has something wrong")
			send_email()
			raise
	else:
		print("dns err")
		send_email()

def check_web(test_name,test_type,url=None):
	if test_type=="FLAG":
		urlflag = urllib2.urlopen(url)
		if "!flag: NAP_2016_Web_Challenge_Part_1" in urlflag.read():
			print("%s is OK , get flag"%test_name)
		else:
			print("web FLAG worng")
			send_email()
			raise
	elif test_type == "txt":
		test = check_output(["dig","+nocomment","+noadditional","+nostats","+noquestion",'txt',url])
		if "NAP_2016_Web_Challenge_Part_1" in test:
			print("%s is OK , WEB TXT is right"%test_name)
		else:
			print("web dns txt is wrong")
			send_email()
			raise

def check_slave(test_name,test_domain):
	test = check_output(["dig","+short","ns",test_domain])
	soa = check_output(["dig","+short","soa",test_domain])
	ns =  test.strip().split("\n")	
	for eachns in ns:
		test_ns_soa = check_output(["dig","+short","soa","@"+eachns,test_domain])
		if soa == test_ns_soa:
			print("the ns %s is fine"%eachns)
		else:
			print("slave serial is not sync")
			#send_email() #maybe wait for some time
			raise

member = [("nctusam.idv.tw.","139.59.102.151")]
while(1):
	for each in member:
		print(bcolors.OKBLUE+"************NOW WE CHECK NA**************"+bcolors.ENDC)
		print("domain name :"+each[0])
		print("ip address :"+each[1])
		print(bcolors.HEADER+"************NA-HW1-2**************"+bcolors.ENDC)
		#test DNS1 CNAME
		DNS1 = 'NAP2016-DNS1.nasa.'+each[0]
		#test DNS2 A record
		DNS2 = 'NAP2016-DNS2.nasa.'+each[0]
		#test WEB1 FLAG
		WEB1_flag = 'http://nap2016-web1.nasa.'+each[0]
		#test WEB1 TXT
		WEB1_DNS_TXT = 'NAP2016-WEB1.nasa.'+each[0]
		check_port("80",each[0],"test_80_port")
		check_port("53",each[0],"test_tcp53_port")
		check_port("53",each[0],"test_udp53_port",udp=True)
		check_dns(DNS1,"test_CNAME","CNAME")
		check_dns(DNS2,"test_A record","A",ip=each[1])
		check_web("test_WEB1_flag","FLAG",url=WEB1_flag)
		check_web("test_WEB1_TXT","txt",url=WEB1_DNS_TXT)
		print(bcolors.OKGREEN+"***********HW1-2 OK!!***************"+bcolors.ENDC)
		print(bcolors.HEADER+"************NA-Slave alive or serial is syn**************"+bcolors.ENDC)
		check_slave("test_salve",each[0])	
		print(bcolors.OKGREEN+"************NA-Slave all is fine**************"+bcolors.ENDC)






		print(bcolors.WARNING+"***********WAIT FOR NEXT CHECK!!***************"+bcolors.ENDC)
		sleep(1800)
	
	
	
