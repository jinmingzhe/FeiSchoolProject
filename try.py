#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import numpy as np 
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Table, MetaData, Column, Integer, String, LargeBinary, Float, DateTime
def my_avg((horizontal, vertical, ordinate), macAddr):   #求出某一坐标下某一mac地址下场强的均值
    conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='feifei_1',
        db ='namename',
        )
    cur = conn.cursor()
    #cur.execute("select * from wifiset")
    MySqlSelectDataCM = "select RSSI from wifidata where horizontal = %s and vertical = %s and ordinate = %s and macAddr = %s"
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
        newlist.append(i[0])   #去掉元组
    print newlist
    intlist = map(int, newlist)
    temp = []
    for i in intlist:
        temp.append(i)
    print temp                  #字符串变为整形
    avg = np.mean(temp)
    print ('chang qiang jun zhi:', avg)
    cur.close()
    conn.commit()
    conn.close()
    #return avg

my_avg((0.6, 6.6, 4), '06:19:70:00:3a:58')
#print m

engine = create_engine("mysql+pymysql://root:feifei_1@localhost/namename",encoding='utf-8', echo=True)
metadata = MetaData()
user = Table('wifidata', metadata,
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
        return "<User(ID='%s',  SSID='%s', RSSI='%s', channel='%s', macAddr='%s', horizontal='%s', vertical='%s', ordinate='%s', time='%s')>" % (self.ID, self.SSID, self.RSSI, self.channel, self.macAddr, self.horizontal, self.vertical, self.ordinate, self.time)
mapper(User, user)

Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
Session = Session_class()  # 生成session实例，相当于游标
#my_user = Session.query(User).filter_by(ID=1).first()  # 查询
#print(my_user.horizontal, my_user.vertical, my_user.ordinate)
mac = []
mac = Session.query(User.macAddr).all()
#print(mac)  #列出mac地址
maclist = []
for i in mac:
    maclist.append(i[0])
#print maclist            #list列表的mac地址
setmaclist = list(set(maclist))
print setmaclist                                       #去重后的mac地址
coo = Session.query(User.horizontal, User.vertical, User.ordinate,).all()
#print coo
setcoo = list(set(coo))
print setcoo                                            #去重后的坐标

