





#!/usr/bin/python
import paramiko
import random
import time
import sys
import atexit      # allowes me to use a wraper around the exit , so i could run some function before termination



''' this script enables the user to send a single/list of commands  via ssh to be executed by a remote host,
	includiing failure detection mechanisem (atexit).
	usage example :: 
		SSH_Func('192.168.33.1',yoav,zubur1,[touch ~/empty.txt , dos2unix ~/empty.txt , chmod  +x ~/empty.txt])
	'''

#examples ::

#command_list_monitor=['chmod +x ~/scripts/asg_monitor.sh','dos2unix ~/scrips/asg_monitor','nohup ~/scripts/asg_monitor.sh &']

#command_list_failover=['chmod +x ~/scripts/failovers4.mail.sh','dos2unix ~/scripts/failovers4.mail.sh', '/scripts/failovers4.mail.sh  &']

#GW_Side_Command_List=[command_list_failover,command_list_monitor]
#Management_Side_Command_List

'''
 script main usage is ~/scripts/failovers4.mail.sh 
 first operator is to choose the action ,  1=asg sgm_admin down   2= asg sgm_admin up 3=reboot sgm   4=asg chassis_admin down  5= asg chassis_admin up    
 second operator is in case we choose 1/2 in the first operator , the second operator is to tell the script on which blade we want to perform this action.
'''


def goodby():
#	''' functions to run upon termination of the program'''
	print ("Preparing to say goodby ...")
	print (" enabling y/n Questionire on the setup")
	SSH_Func(hostname,username,password,'g_all -a rm /etc/.asg_auto_confirm')
	print ("ending in 2 seconds ..")
	time.sleep(2)
	return	
	
	

def Exit_Coder(argument):
	''' this function receives exit status and returns it's meaning in text '''
	switcher={ 
		0: "Success",
		1:"General Error",
		2:"miss-use of shell",
		126:"cannot execute , apparently no permissions",
		127:"command not found \ file doesn't exist",
		130:"terminated by CTRL+C",
	}
	return switcher.get(argument)

def command_to_execute(session, cmd_to_exec):
	atexit.register(goodby)	
	stdin, stdout, stderr =session.exec_command(cmd_to_exec)
	out=stdout.readlines()
	exit_status = stdout.channel.recv_exit_status()
	print("executed command \'{0} \' with the following exit code : \'{1}\'".format( cmd_to_exec , Exit_Coder(exit_status) ))
	if (exit_status!=0):exit()                # if command failed to execute , quit program
	return out


def SSH_Func( HostName , UserName , Password , Command_List ):
	''' this function's Purpose is to run multiple commands on remote 	Host via ssh.
	usage example is :
	SSH_Func('192.168.33.1',yoav,zubur1,[touch ~/empty.txt , dos2unix ~/empty.txt , chmod  +x ~/empty.txt])
	* FYI : this function will also accept a single command to run , or even a list of lists of commands to run.
	'''	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=HostName, username=UserName,password=Password  )
	if isinstance(Command_List , list):     ## all of the following if and for are to detect if the command argument is a single command , a list of commands , or a list of lists .
		for i in command_list:
			if isinstance( i , list):
				for j in i:
					output=command_to_execute(ssh , j)
			else:
				output=command_to_execute(ssh , i)
	else:
		output=command_to_execute(ssh , Command_List)
	ssh.close()
	return output

def get_random_sgm_id(hostname,username,password):
	ret_val=SSH_Func(hostname,username,password,'asg stat -i active_ids')
	val=str(random.choice(ret_val).strip())
	return val
	
	
	
