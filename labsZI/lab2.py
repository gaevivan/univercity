#!/usr/bin/python

import threading
import re
import time


VAL = 'valid'
INV = 'invalid'
NOTYPE = 'notype'


class Data:
    def __init__(self, type, value, time):
        self.type = type
        self.value = value
        self.time = time
    def __str__(self):
        return '{value}'.format(
            value = self.value
        )
    def __repr__(self):
        return self.__str__()

def reading(count):
    i = 0
    file = open('input_data', 'r')
    for line in file:
        if i == count:
            r2c.append(line.replace('\n',''))
        i += 1
    if count < 10:
        threading.Timer(0.5, reading, args=(count+1,)).start()

def checking():
    if len(r2c) > 0:
        prec2c = []
        checkitem = r2c.pop(0)
        if len(r2c) > 0:
            while len(r2c) > 0:
                r2c.pop(0)
        match = re.findall( pattern, checkitem )
        for item in match:
            prec2c.append(Data(VAL, item, 0))
            checkitem = checkitem.replace( item, ' ' )
        for item in checkitem.split( ' ' ):
            if item != '':
                prec2c.append(Data(INV, item, 0))
        c2c.append(prec2c)
        threading.Timer(1, checking).start()

def cleaning():
    if len(c2c) > 0:
        prec2l = []
        prec2l.extend(c2c.pop(0))
        if len(c2c) > 0:
            while len(c2c) > 0:
                c2c.pop(0)
        flag = True
        while flag:
            i = False
            for item in prec2l:
                if item.type == INV:
                    prec2l.remove(item)
            for item in prec2l:
                if item.type == INV:
                    i = True
            if i:
                flag = True
            else:
                flag = False
        c2l.append(prec2l)
        threading.Timer(2, cleaning).start()

def logging(count, data_out):
    if len(c2l) != 0:
        predata = c2l.pop(0)
        if len(c2l) > 0:
            while len(c2l) > 0:
                c2l.pop(0)
        for item in predata:
            data_out += item.value
        count += 1
        data_out += '\n'
        print '\nLOG('+str(count*10)+'%): '+ data_out
        if (len(c2l)+len(c2c)+len(r2c)) == 0:
            print 'Terminated...'
        threading.Timer(4, logging, args=(count,data_out,)).start()

if __name__ == '__main__':
    r2c = []
    c2c = []
    c2l = []
    t = 0.5
    pattern = r'[\d]+\.[\d]+|[A-z]+'
    threading.Timer(t, reading, args=(0,)).start()
    threading.Timer(t*2, checking).start()
    threading.Timer(t*4, cleaning).start()
    threading.Timer(t*8, logging, args=(0,'\n',)).start()
