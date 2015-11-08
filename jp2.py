#!/usr/bin/python
#coding:utf-8

__author__ = 'laopangzhang'

from conf import ConnList
import  os
from output import *
import readchar
import time
import subprocess
from blessings import Terminal



def getidfromfile(idsifle):
    f = open(idsifle,'r')
    ids = f.read()
    return ids

def genhostlist():
    os.system("echo '' > host.list")
    id = 0
    for host in ConnList:
        id += 1
        host['id'] = str(id)
        hostname = host.get('host')
        remarks = host.get('remarks')
        f=open("host.list",'a')
        f.write(str(id) + ":" + hostname + "     备注   "  +  "|" + remarks  + '\n')
        f.close()



def getmatchlist(ids):
    id = 0
    hostids = ids.strip().split(":")
    SelectedList = []
    for host in ConnList:
        id += 1
        host['id'] = str(id)
        for hostid in hostids:
          if hostid == host['id']:
             SelectedList.append(ConnList[id-1])
    return SelectedList




def list():
    id = 0
    for element in ConnList:
        id += 1
        element['id'] = id
        hostname = element.get('host')
        remarks = element.get('remarks')
        if element['isSelected']:
            print use_style("==>>" + "   "  + str(id) + ":" + hostname + "|" + "     备注   " + "|" + remarks + "  " +"<<==", mode='bold',fore='red')
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
            connhost_bykey(ip,user,key,port)
        else:
            pwd = selhost.get('password')
            connhost_bypwd(ip,user,pwd,port)
    #exit()

#
#list()
#print findhost(3)
#
#
_UP = "'k'"
_DOWN = "'j'"
_ESC1 = "'q'"
_ESC2 = "'q'"
_ENTER = "'\\r'"

keystr = ""
seleid = ""





def getscreentofile(host):
    f = open("selectedhost.list",'w')
    print >>f,host
    f.close()

def interactsys(cmd):
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buff = ""
    while True:
        line = p.stdout.readline()
        if line == '' and p.poll() != None:
            break
        buff += line
    return buff.strip()
t = Terminal()
def printstyle(cmd,keyword):
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buff = ""
    while True:
        line = p.stdout.readline().strip()
        outputs = line.split(keyword)
        colortext = ""
        for output in outputs:
           colortext += "{t.normal}" + output.strip() + '{t.red}' + "{t.bold}" + keyword.strip() + "{t.normal}".strip()
        print colortext[0:-((len(keyword + "{t.normal}")  ))].strip().format(t=t)
        #print t.wingo(2).strip()
           #print output,
           #print use_style(keyword,mode = 'bold',fore = 'red'),

        if line == '' and p.poll() != None:
            break
genhostlist()


while True:
    os.system("clear")
    os.system("cat host.list")
    keyword = ""
    while True:
        key =  repr(readchar.readchar())
        if key[1] == "*" :
            keyword = keyword[0:-1]
            if len(keyword) == 0:
               os.system("clear")
               print use_style("Warnning!!!NO char to delete!",mode = 'bold',fore = 'red' )
               os.system("cat host.list")
               continue
        elif key[1] == " ":
            if len(keyword) == 0:
                getid_cmd = "cat host.list |grep -i '%s' |awk -F : '{print $1}'|sed ':a;N;$!ba;s/\\n/:/g' > ids.hosts " % (keyword)
                seleid = os.system(getid_cmd)

            break
        else:
            keyword += key[1]


        os.system("clear")
        print keyword
        cmd = "cat host.list | grep -i '%s'" % (keyword)
        getselnum = "cat host.list | grep -i '%s'|wc -l" % (keyword)
        getid_cmd = "cat host.list |grep -i '%s' |awk -F : '{print $1}'|sed ':a;N;$!ba;s/\\n/:/g' > ids.hosts " % (keyword)
        if interactsys(getselnum) == "0":
            print use_style("Warnning!!!No host has matched!,press BackSpace",mode = 'bold',fore = 'red' )
            continue
        printstyle(cmd,keyword)
        seleid = os.system(getid_cmd)

    break


ids = getidfromfile('ids.hosts')

print ids

ConnList = getmatchlist(ids)
'''
for host in ConnList:
    print host
'''


running=True
ConnList[0]['isSelected'] = True



while running:
    os.system('clear')
    list()
    print("Press 'Q' or 'q' to quit:\n")
    cmd = repr(readchar.readchar())
    if cmd == "'<'":
        keystr += cmd

    if (cmd == _ESC1 or cmd == _ESC2):
        break;
    elif cmd.isdigit():
        if (int(cmd) >= 0 and int(cmd) <= 100):
            if ConnectHost(int(cmd)):
                continue



    elif (cmd == _DOWN):
        if ConnList[-1].get('id') == GetSelected():
            CurHostid = GetSelected()
            SetIDUnSelected(CurHostid)
            ConnList[0]['isSelected'] = True
            continue
        CurHostid = GetSelected()
        SetIDUnSelected(CurHostid)
        SetIDSelected(CurHostid + 1)

    elif (cmd == _UP):
        if ConnList[0].get('id') == GetSelected():
            CurHostid = GetSelected()
            SetIDUnSelected(CurHostid)
            ConnList[-1]['isSelected'] = True
            continue
        CurHostid = GetSelected()
        SetIDUnSelected(CurHostid)
        SetIDSelected(CurHostid - 1)

    elif (cmd == _ENTER):
        selhost = findhost(GetSelected())
        id = selhost['id']
        ConnectHost(id)





    else:
        continue;





