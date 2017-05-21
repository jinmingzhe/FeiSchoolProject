#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Table, MetaData, Column, Integer, String, LargeBinary, Float, DateTime
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
print(Session.query(User.horizontal,User.vertical,User.ordinate).all() )