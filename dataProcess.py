#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import numpy as np

def my_avg(horizontal, vertical, ordinate, macAddr):
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='feifei_1',
        db ='wifi',
        )
    cur = conn.cursor()
    #cur.execute("select * from wifiset")
    MySqlSelectDataCM = "select RSSI from wifiset where horizontal = %s and vertical = %s and ordinate = %s and macAddr = %s"
    #aa = cur.execute("select RSSI from wifiset where horizontal = %s and vertical = %s and ordinate = %s and macAddr = %s",[x,y,z,h])
    aa = cur.execute(MySqlSelectDataCM,[horizontal,vertical,ordinate,macAddr])
    print aa
    info = cur.fetchmany(aa)
    list = []
    for ii in info:
        list.append(ii)
    print list
    newlist = []
    for i in list:
        newlist.append(i[0])
    print newlist
    intlist = map(int, newlist)
    temp = []
    for i in intlist:
        temp.append(i)
    print temp
    avg = np.mean(temp)
    print ('chang qiang jun zhi:', avg)
    cur.close()
    conn.commit()
    conn.close()
    return avg

m = my_avg(1, 2, 3, '88:25:93:08:73:0c')
print m