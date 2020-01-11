import os
import pymysql
from time import strftime,gmtime
import time
import datetime
date_time=(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
db = pymysql.connect("localhost","root","czl1041484348","devops")
cursor = db.cursor()

sql_select_ip = """
            select * from Host_server_status where ip='{}'
        """
sql_create_ip="""
            insert into Host_server_status(ip,status,Damage_times,create_time,last_time) values(%s,%s,%s,%s,%s)
            """
sql_update_Damageadd="""
            update Host_server_status set Damage_times=Damage_times+1,last_time='{}' where ip='{}'

            """
sql_update_good="""
            update Host_server_status set status=0,Damage_times=0,last_time='{}' where ip='{}'
            """
host_file = open('/opt/sumscope/devops/scripts/hosts')
fping_host=[]
while(True):
    host_files = host_file.readline()
    if host_files == '':
        break
    temp = host_files.split()[1]
    fping_host.append(temp.split('=')[1])

host_file.close()
for ip_host in fping_host:
    val = os.popen(("/usr/sbin/fping {}  -u ").format(ip_host))
    val_data = val.read()
    if  val_data != '':
        try:
            cursor.execute(sql_select_ip.format(str(ip_host)))
            cursor.execute(sql_update_Damageadd.format(date_time,str(ip_host)))
            db.commit()
        except:
            cursor.execute(sql_create_ip,(str(ip_host),'1','1',date_time,date_time))
            db.commit()
    if  val_data == '':
        try:
            cursor.execute(sql_select_ip.format(str(ip_host)))
            cursor.execute(sql_update_good.format(date_time,str(ip_host)))
        except:
            cursor.execute(sql_create_ip,(str(ip_host),'0','0',date_time,date_time))
            db.commit()



db.close()