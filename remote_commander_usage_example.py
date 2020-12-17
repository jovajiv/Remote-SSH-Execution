#!/usr/bin/python



import os,sys,time
import atexit,threading
# adds the current working directory into the python module path.
sys.path.insert(0,os.getcwd) 
from Python_remote_commander import SSH_Func,get_random_sgm_id



gateway_ip = 'x.x.x.x'
username_gw = useruser
password_gw = 123456

mgmt_ip = 'x.x.x.x'
username_mgmt = useruser
password_mgmt = 123456

def goodby():
	''' functions to run upon termination of the program'''
	print "Preparing to say goodby ..."
	print " enabling y/n Questionire on the setup"
	SSH_Func(gateway_ip,password_gw,password,'g_all -a rm /etc/.asg_auto_confirm')
	print "ending in 2 seconds .."
	time.sleep(2)
	return

def Asg_Monitor():
	counter=1
	while 1:
		SSH_Func(gateway_ip,username_gw,password_gw,'~/scripts/asg_monitor.sh '+str(counter))
		counter+=1
		time.sleep(1800)

def Failovers_Reboot():
	while 1:
		SSH_Func(gateway_ip,password_gw,password_gw,'g_all -a touch /etc/.asg_auto_confirm')
		#put sgm in down state
		SGM_ID=get_random_sgm_id(gateway_ip,password_gw,password_gw)
		SSH_Func(gateway_ip,password_gw,password_gw,'~/scripts/failovers4.mail.sh 1 '+SGM_ID )
		time.sleep(300)
		#put sgm in up state
		SSH_Func(gateway_ip,password_gw,password_gw,'~/scripts/failovers4.mail.sh 2 '+SGM_ID )
		time.sleep(300)
		#reboot  sgm 
		SGM_ID=get_random_sgm_id(gateway_ip,password_gw,password_gw)
		SSH_Func(gateway_ip,password_gw,password_gw,'~/scripts/failovers4.mail.sh 3 '+SGM_ID )
		time.sleep(600)
		#put chassis in down state
		SSH_Func(gateway_ip,password_gw,password_gw,'~/scripts/failovers4.mail.sh 4' )
		time.sleep(300)
		#put chassis in up state
		SSH_Func(gateway_ip,password_gw,password_gw,'~/scripts/failovers4.mail.sh 5' )
		time.sleep(300)

def Install_Policy():

	print ' initiating Policy Installation  .....'
	SSH_Func(mgmt_ip,username_mgmt,password_mgmt,'~/BACKUP-FROM-PREVIOUS-MDS/install_policy_longivity.sh ')
	

def Vsx_Push():
	print ' initiating VSX_Push  .....'
	while 1:
		SSH_Func(mgmt_ip,username_mgmt,password_mgmt,'~/BACKUP-FROM-PREVIOUS-MDS/vsx_provisioning_automation_v3.5.sh longivity_Remote')
		time.sleep(3600)
	
	
	
def GW_Scripts():
	monitor=threading.Thread(target=Asg_Monitor)
	failover=threading.Thread(target=Failovers_Reboot)	
	print ' initiating Monitoring  .....'
	monitor.start()
	print ' initiating Failover  .....'
	failover.start()	
	print ' Monitor Join  .....'
#	monitor.join()
	print ' Failover Join  .....'
#	failover.join()
        


def MGMT_Scripts():
	policy=threading.Thread(target=Install_Policy)
	vsx=threading.Thread(target=Vsx_Push)
	
	policy.start()
	vsx.start()
	
#	policy.join()
#	vsx.join()
	
	
def main():
	print ' initiating GW side scripts .....'
	GW_Scripts()
	print ' initiating MGMT side scripts .....'
	MGMT_Scripts()
print 'starting Main'
main()
	
