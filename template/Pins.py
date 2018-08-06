import os, datetime,time

def Init():
	os.system("gpio mode 0 out") #LED 1
	os.system("gpio mode 2 up")
	os.system("gpio mode 3 out") #LED 2
	os.system("gpio mode 4 up")
	os.system("gpio mode 5 out") #LED 3
	os.system("gpio mode 6 up")
	global time1,time2,time3,on1,on2,on3,tot_time1,tot_time2,tot_time3,last_sess,tot,lines
	global f,l	#Setting it global as it is to be used in other functions too
	f = open("log.txt","a+") # Opening the log file
	l = open("stat.txt","r+") # Opening the stat file
	tot_time1 = 0 
	tot_time2 = 0 
	tot_time3 = 0
	on1=False
	on2=False
	on3=False
	lines = l.readlines()
	tot = [int(s) for s in lines[0].split() if s.isdigit()] #Fetching the stats for the total sessions
	last_sess = [int(s) for s in lines[1].split() if s.isdigit()] #Fetching the stats for the last session
	tot[0] += last_sess[0]
	tot[1] += last_sess[1]
	tot[2] += last_sess[2]
	
def retStat():
	global tot,last_sess
	return tot,last_sess
	
def LogMaintain(led,status):
	now = datetime.datetime.now()
	f.write("%s %s %s\n" % (now.strftime("%d-%m-%Y %H:%M:%S"), led, status)) #Write function doesn't work in the same way as print so we have to use %s and string tuple to do this
	
# Switches on the LED depending on the requirement
def LEDon(lid):
	global time1,time2,time3,on1,on2,on3
	if int(lid) == 1:
		os.system("gpio write 0 on")
	elif int(lid) == 2:
		os.system("gpio write 3 on")
	elif int(lid) == 3:
		os.system("gpio write 5 on")
	elif int(lid) == 4:
		os.system("gpio write 0 on")
		os.system("gpio write 3 on")
		os.system("gpio write 5 on")
	
	#Sets the time when the LED is switched on
	if not on1 and (int(lid)==1 or int(lid)==4):
		time1 = time.time()
		on1=True
	if not on2 and (int(lid)==2 or int(lid)==4):
		time2 = time.time()
		on2=True
	if not on3 and (int(lid)==3 or int(lid)==4):
		time3 = time.time()
		on3=True	
	LogMaintain(lid,"ON")

# Switches off the LED depending on the requirement	
def LEDoff(lid):
	global on1,on2,on3,tot_time1,tot_time2,tot_time3
	if int(lid) == 1:
		os.system("gpio write 0 off")
	elif int(lid) == 2:
		os.system("gpio write 3 off")
	elif int(lid) == 3:
		os.system("gpio write 5 off")
	elif int(lid) == 4:
		os.system("gpio write 0 off")
		os.system("gpio write 3 off")
		os.system("gpio write 5 off")
	
	#When LED is switched off, updates the on time
	if on1 and (int(lid)==1 or int(lid)==4):
		tot_time1+= (time.time()-time1)//1
		on1=False
	if on2 and (int(lid)==2 or int(lid)==4):
		tot_time2+= (time.time()-time2)//1
		on2=False
	if on3 and (int(lid)==3 or int(lid)==4):
		tot_time3+= (time.time()-time3)//1
		on3=False
	LogMaintain(lid,"OFF")
			
def ReadButton(bid):
	# Reading from the pins then geting the output from the commandline
	led1=os.popen("gpio read 2").read()
	led2=os.popen("gpio read 4").read()
	led3=os.popen("gpio read 6").read()
	flag=0
	
	#Setting the flag so that it returns only the one that is needed.
	if int(bid) == 1 and int(led1) == 1:
		flag=1
	elif int(bid) == 2 and int(led2) == 1:
		flag=1
	elif int(bid) == 3 and int(led3) == 1:
		flag=1
	elif int(bid) == 4 and int(led1) == 1 and int(led2) == 1 and int(led3) == 1:
		flag=1
	if int(flag) == 1:  
		return True #Sending True when Button is ON
	else:
		return False #Sending True if Button is OFF
	
#This functions closes the open file handles, writes the updates into the stat file and resets the pins so as to bring it to its original state	
def Cleanup():
	global time1,time2,time3,on1,on2,on3,tot_time1,tot_time2,tot_time3,f,l,tot,lines
	LEDoff(4);
	l.close
	
	#Opening via 'w' mode so that the original file is rewritten
	l=open("stat.txt","w")
	l.write("%s %s %s\n" %(tot[0],tot[1],tot[2]))
	l.write("%s %s %s" %(int(tot_time1),int(tot_time2),int(tot_time3)))
	os.system("gpio mode 0 in")
	os.system("gpio mode 3 in")
	os.system("gpio mode 5 in")
	l.close
	f.close # Closing the log file
