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




pwd = os.path.split(os.path.realpath(__file__))[0]
hostlist = pwd +  "/host.list"
selectedhost =   pwd + "/selectedhost.list"
idshost = pwd + "/ids.hosts"
autologin_key = pwd + '/auto_key_login.exp'
autologin_pwd = pwd + '/auto_login.exp'

def getidfromfile(idsifle):
    f = open(idsifle,'r')
    ids = f.read()
    f.close
    return ids

def genhostlist():
    os.system("cat /dev/null > %s" % (hostlist) )
    id = 0
    for host in ConnList:
        id += 1
        host['id'] = str(id)
        hostname = host.get('host')
        remarks = host.get('remarks')
        f=open(hostlist,'a')
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
    os.system(autologin_key + ' ' + ip + ' ' + user +  ' '  + key + ' ' + port)

def connhost_bypwd(ip,user,pwd,port):
    os.system(autologin_pwd+ ' ' + ip + ' ' + user +  ' '  + pwd + ' ' + port)

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

_UP = "'k'"
_DOWN = "'j'"
_ESC1 = "'q'"
_ESC2 = "'q'"
_ENTER = "'\\r'"

keystr = ""
seleid = ""





def getscreentofile(host):
    f = open(selectedhost,'w')
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


def printstyle(cmd,keyword):
    t = Terminal()
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
    p.wait()
    buff = ""
    while True:
        line = p.stdout.readline().strip()
        outputs = line.split(keyword)
        colortext = ""
        for output in outputs:
           colortext += "{t.normal}" + output.strip() + '{t.red}' + "{t.bold}" + keyword.strip() + "{t.normal}".strip()
        print colortext[0:-len(keyword + "{t.normal}")].strip().format(t=t)
        #print t.wingo(2).strip()
           #print output,
           #print use_style(keyword,mode = 'bold',fore = 'red'),

        if line == '' and p.poll() != None:
            break

genhostlist()
os.system("clear")
os.system("cat %s" % (hostlist))
limit = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_-:*.|\/\\"
keyword = ""
while True:
    key =  repr(readchar.readchar())
    if not (key[1]  in limit):
       os.system("clear")
       print use_style("Warnning!! Invalide Char %s!" % (key[1]),mode = 'bold',fore = 'red' )
       print keyword
       os.system("cat %s" % (hostlist))
       continue
    elif key[1] == "*" :
        keyword = keyword[0:-1]
        if len(keyword) == 0:
           os.system("clear")
           print use_style("Warnning!!!NO char to delete!",mode = 'bold',fore = 'red' )
           os.system("cat %s" % (hostlist))
           continue
    elif key == _ENTER:
        if len(keyword) == 0:
            getid_cmd = "cat hostlist |grep '%s' |awk -F : '{print $1}'|sed ':a;N;$!ba;s/\\n/:/g' > %s " % (keyword,idshost)
            seleid = os.system(getid_cmd)
        break
    else:
        keyword += key[1]


    getselnum = "cat %s | grep  '%s'|wc -l" % (hostlist,keyword)
    if interactsys(getselnum) == "0":
        os.system("clear")
        print use_style("Warnning!!!No host has matched to %s!" % keyword,mode = 'bold',fore = 'red' )
        continue

    os.system("clear")
    print keyword
    cmd = "cat %s | grep  '%s'" % (hostlist,keyword)
    getid_cmd = "cat %s |grep  '%s' |awk -F : '{print $1}'|sed ':a;N;$!ba;s/\\n/:/g' > %s " % (hostlist,keyword,idshost)

    printstyle(cmd,keyword)
    #os.system(cmd)
    seleid = os.system(getid_cmd)


ids = getidfromfile(idshost)


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




