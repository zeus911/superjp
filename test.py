#!/usr/bin/python
#coding:utf-8

import readchar
import time
import subprocess
import string


from blessings import Terminal

'''
t = Terminal()

print t.bold('Hi there!')
print t.bold_red_on_bright_green('It hurts my eyes!')

print '{t.bold}All your {t.red}bold and red base{t.normal}'.format(t=t)
print t.wingo(2)
'''

a='laopangzhang'
print a.find('zhang')

'''
cmd = "cat host.list|wc -l"
def interactsys(cmd):
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buff = ""
    while True:
        line = p.stdout.readline()
        if line == '' and p.poll() != None:
            break
        buff += line
    return buff.strip()

#print cmd[0:-1]
'''

