#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import math
import numpy as np 
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Table, MetaData, Column, Integer, String, LargeBinary, Float, DateTime


class User(object):
    def __init__(self, ID, SSID, RSSI, channel, macAddr, horizontal, vertical, ordinate, time):
        self.ID = ID
        self.SSID = SSID
        self.RSSI = RSSI
        self.channel = channel
        self.macAddr = macAddr
        self.horizontal = horizontal
        self.vertical = vertical
        self.ordinate = ordinate
        self.time = time
    def __repr__(self):
        return "<User(ID='%s',  SSID='%s', RSSI='%s', channel='%s', macAddr='%s', horizontal='%.2f', vertical='%.2f', ordinate='%.2f', time='%s')>" % (self.ID, self.SSID, self.RSSI, self.channel, self.macAddr, self.horizontal, self.vertical, self.ordinate, self.time)


#mean
def my_avg((horizontal, vertical, ordinate), macAddr):   #求出某一坐标下某一mac地址下场强的均值
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
    #print aa
    info = cur.fetchmany(aa)
    list = []
    for ii in info:
        list.append(ii)
    #print list
    newlist = []
    for i in list:
        newlist.append(i[0])                                                          #去掉元组
    #print newlist
    intlist = map(int, newlist)
    temp = []
    for i in intlist:
        temp.append(i)
    #print temp                                                                         #字符串变为整形
    avg = np.mean(temp)                                                                 #求均值
    vare = np.var(temp)                                                                 #求方差
    #print (avg,vare)
    cur.close()
    conn.commit()
    conn.close()           
    return (avg,vare,len(temp))                                                         #返回均值、方差、rssi的长度

#my_avg((0.6, 6.6, 4), '06:19:70:00:3a:58')
#print m

engine = create_engine("mysql+pymysql://root:feifei_1@localhost/wifi",encoding='utf-8', echo=True)
metadata = MetaData()
user = Table('wifiset', metadata,
            Column('ID', Integer, primary_key=True),
            Column('SSID', LargeBinary(255)),
            Column('RSSI', LargeBinary(255)),
            Column('channel', LargeBinary(255)),
            Column('macAddr', LargeBinary(255)),
            Column('horizontal', Float),
            Column('vertical', Float),
            Column('ordinate', Float),
            Column('time', DateTime),
        )

mapper(User, user)
Session_class = sessionmaker(bind=engine)                                            # 实例和engine绑定
Session = Session_class()                                                            # 生成session实例，相当于游标
#my_user = Session.query(User).filter_by(ID=1).first()  # 查询
#print(my_user.horizontal, my_user.vertical, my_user.ordinate)
mac = []
mac = Session.query(User.macAddr).all()
#print(mac)                                                                            #列出mac地址
maclist = []
for i in mac:
    maclist.append(i[0])
#print maclist                                                                         #list列表的mac地址
setmaclist = list(set(maclist))
#print setmaclist                                                                       #去重后的mac地址
coo = Session.query(User.horizontal, User.vertical, User.ordinate,).all()
#print coo
setcoo = list(set(coo))
print setcoo
D = {}  
print 'start print my_avg'                                                              #去重后的坐标
for x in setcoo: 
    for z in setmaclist:
        #print 'print my_avg ==> ', my_avg(x,z)                                         #这里需要去判定x坐标下是否存在mac地址z
        D[(x,z)] = my_avg(x,z)
        if math.isnan(my_avg(x,z)[0]):
            del D[(x,z)]

#for k in D:
    #else:
        #print k, ':', D[k]
for k in D:
    for f in D:
        if k != f:
            #print [D[k],D[f]]
            w = (D[k],D[f])
            print w
            print w[0][1]                                                                            #输出字典
    #print k, ':', D[k]
