# -*- coding: utf-8 -*-
import subprocess
import MySQLdb
import time

#########################################################
now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
sql = "INSERT INTO tbldata(murl,dns_lookup_time,connect_time,download_speed,total_time,http_code,mdate_time,idx) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"


#######################################################33






connection = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "password", db = "APM")
cursor = connection.cursor()
cursor.execute ("SELECT url,idx FROM tblurl WHERE idx='XXX'")

# fetch a single row using fetchone() method.
for(url,idx) in cursor:
        comd = 'curl -o /dev/null -skw "%{time_namelookup}|%{time_connect}|%{speed_download}|%{time_total}|%{http_code}" ' +url

        procs = subprocess.Popen(comd, shell=True, stdout=subprocess.PIPE)
        output = procs.stdout.read()
        procs.stdout.close()
        procs.wait()
        result = output.split("|")
        hwan = result[2]
        hwan = hwan.replace(".000", "")
        hwan = int(hwan) / 1024 / 1024
        msg = "URL: " + url + "s / NSLookup Time: "+result[0]+"s / Connect Time: "+result[1]+"s / Download Speed: "+str(hwan)+"MB/s / Total: "+result[3]+"s / Http Status: "+result[4]
#       print msg
        re = cursor.execute("INSERT INTO tbldata(murl,dns_lookup_time,connect_time,download_speed,total_time,http_code,mdate_time,idx) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(url,result[0],result[1],str(hwan),result[3],result[4],now,idx))
        cursor.execute(sql,(url,result[0],result[1],str(hwan),result[3],result[4],now,idx))
        connection.commit()

cursor.close ()
# close the connection
connection.close ()



~

