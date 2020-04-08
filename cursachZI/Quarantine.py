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

class Quarantine:
    def __init__(self, loadtext):
        self.text = loadtext
        self.outtext = ''
        self.r2c = []
        self.c2c = []
        self.c2l = []
        self.predata = []
        self.all = 0
        self.t = 0.03
        self.pattern = r'[\d]+\.[\d]+|[A-z]+'

    def reading(self, count):
        i = 0
        for item in self.text:
            i += 1
        self.all = i
        i = 0
        for item in self.text:
            if i == count:
                self.r2c.append(item)
            i += 1
        if count < self.all:
            threading.Timer(self.t, self.reading, args=(count+1,)).start()

    def checking(self):
        if len(self.r2c) > 0:
            prec2c = []
            checkitem = self.r2c.pop(0)
            if len(self.r2c) > 0:
                while len(self.r2c) > 0:
                    self.r2c.pop(0)
            match = re.findall( self.pattern, checkitem )
            for item in match:
                prec2c.append(Data(VAL, item, 0))
                checkitem = checkitem.replace( item, ' ' )
            for item in checkitem.split( ' ' ):
                if item != '':
                    prec2c.append(Data(INV, item, 0))
            self.c2c.append(prec2c)
            threading.Timer(self.t, self.checking).start()

    def cleaning(self):
        if len(self.c2c) > 0:
            prec2l = []
            prec2l.extend(self.c2c.pop(0))
            if len(self.c2c) > 0:
                while len(self.c2c) > 0:
                    self.c2c.pop(0)
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
            self.c2l.append(prec2l)
            threading.Timer(self.t, self.cleaning).start()

    def logging(self, count, data_out):
        self.outtext = ''
        if len(self.c2l) != 0:
            self.predata = self.c2l.pop(0)
            if len(self.c2l) > 0:
                while len(self.c2l) > 0:
                    self.c2l.pop(0)
            for item in self.predata:
                data_out += item.value + ' '
            count += 1
            self.predata = []
            #self.outtext = data_out
            #print 'LOG('+str(count*(100/self.all))+'%): '+ data_out
            threading.Timer(self.t, self.logging, args=(count,data_out,)).start()
        else:
            self.outtext = data_out
            if self.outtext == '':
                self.outtext = 'Failed'
            else:
                print '\nLOG('+str(count*(100/self.all))+'%) ', self.outtext, '\n----------------------------------------\n'

    def start(self):
        threading.Timer(self.t, self.reading, args=(0,)).start()
        threading.Timer(self.t*2, self.checking).start()
        threading.Timer(self.t*3, self.cleaning).start()
        threading.Timer(self.t*4, self.logging, args=(0,'',)).start()
