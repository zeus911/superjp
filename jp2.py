#!/usr/bin/python
#coding:utf-8

__author__ = 'laopangzhang'

from conf import *
import  os
from output import *


running=True
ConnList[0]['isSelected'] = True

def list():
    id = 0
    for element in ConnList:
        id += 1
        element['id'] = id;
        hostname = element.get('host')
        remarks = element.get('remarks')
        if element['isSelected']:
            print use_style(str(id) + ":" + hostname + "|" + "     备注   " + "|" + remarks, mode='bold',fore='red')
        else:
            print use_style(str(id) + ":" + hostname + "|" + "     备注   " + "|" + remarks, fore='green')



def findhost(num):
    for host in ConnList:
        if (host.get('id') == num):
            return host


def GetSelected():
    for host in ConnList:
        if host.get('isSelected'):
            return host.get('id')

def connhost_bykey(ip,user,key,port):
    os.system('auto_key_login.exp' + ' ' + ip + ' ' + user +  ' '  + key + ' ' + port)

def connhost_bypwd(ip,user,pwd,port):
    os.system('auto_login.exp' + ' ' + ip + ' ' + user +  ' '  + pwd + ' ' + port)

def SetIDSelected(id):
    host = findhost(id)
    host['isSelected'] = True

def SetIDUnSelected(id):
    host = findhost(id)
    host['isSelected'] = False

def ConnectHost(id):
    selhost = findhost(id)
    ip = selhost.get('host')
    user = selhost.get('user')
    port = selhost.get('port')

    remark = selhost.get('remarks')
    print 'Are sure you want to Connect to host:',
    print use_style(ip + " " + remark, fore='red'),
    print '(Y/n)'
    conncmd = raw_input()
    if (conncmd == 'n' or conncmd == 'N'):
        return False
    else:
        if selhost.get('key'):
            key = selhost.get('key')
            print key
            connhost_bykey(ip,user,key,port)
        else:
            pwd = selhost.get('password')
            print pwd
            connhost_bypwd(ip,user,pwd,port)

#
#list()
#print findhost(3)
#
#


while running:
    os.system('clear')
    list()
    cmd = raw_input("Press 'Q' to quit:\n")
    if (cmd == 'q'):
        break;
    elif cmd.isdigit():
        if (int(cmd) >= 0 and int(cmd) <= 100):
            if ConnectHost(int(cmd)):
                continue



    elif (cmd == ''):
        if ConnList[-1].get('id') == GetSelected():
            CurHostid = GetSelected()
            SetIDUnSelected(CurHostid)
            ConnList[0]['isSelected'] = True
            continue
        CurHostid = GetSelected()
        SetIDUnSelected(CurHostid)
        SetIDSelected(CurHostid + 1)

    elif (cmd == 'c' or cmd == 'C'):
        selhost = findhost(GetSelected())
        id = selhost['id']
        ConnectHost(id)





    else:
        continue;








