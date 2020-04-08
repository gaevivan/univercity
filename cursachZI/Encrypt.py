#!/usr/bin/python

import random
import math

eng = ' ABCDEFGHIJLMNOPQRSTUVWZYZ' #alphabet
simple = [3,5,7,11,13,17,19,23,29] #spisok prostih chisel

class Contact:

    def __init__(self, text, key):
        self.text = text
        self.key = key
        self.keyRSA = []

    def egcd(self, a,b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular ex')
        else:
            return x % m

    def getkeyRSA(self, contact):
        p = random.choice(simple)
        q = random.choice(simple)
        while q == p:
            q = random.choice(simple)
        n = p*q
        fn = (p-1)*(q-1)
        e = random.choice(simple) 
        while e >= fn:
            e = random.choice(simple)
        d = self.modinv(e, fn)
        print '-----Public wire-----\nSent(->): ', e, n
        contact.keyRSA.append(d)
        contact.keyRSA.append(n)
        self.keyRSA.append(e)
        self.keyRSA.append(n)

    def getkey(self, contact):
        p = random.randint(2, 60)
        n = random.randint(2, 60)
        a = random.randint(2, 60)
        L0 = pow(p, a, n)
        print '\n-----Public wire-----\nSent(->): ', p, n, L0
        b = random.randint(2, 60)
        Lk = pow(p, b, n)
        print 'Sent(<-): ', Lk
        self.key = pow(L0, b, n)
        while self.key > 25:
            self.key = self.key - 25
        contact.key = pow(Lk, a, n)
        while contact.key > 25:
            contact.key = contact.key - 25

    def encrypt(self):
        newtext = ''
        for char in self.text:
            newtext += str( eng.index( char ) + self.key ) + ' '
        self.text = newtext

    def transcript(self):
        newtext = self.text.split()
        self.text = ''
        for char in newtext:
            self.text += eng[ int( char ) - self.key ]

    def send(self, contact):
        #shifruem
        self.encrypt()
        #otpravlyaem
        contact.text = self.text
        print 'Sent(->): ', self.text, '\n---------------------'
        #rasshifrovivaem
        self.transcript()
        contact.transcript()

    def encryptRSA(self):
        newtext = ''
        for char in self.text:
            newtext += str(pow(eng.index(char), self.keyRSA[0], self.keyRSA[1])) + ' '
        self.text = newtext

    def transcriptRSA(self):
        newtext = self.text.split()
        self.text = ''
        for char in newtext:
            self.text += str(eng[pow(int(char), self.keyRSA[0], self.keyRSA[1])])

    def sendRSA(self, contact):
        #shifruem
        self.encryptRSA()
        #otpravlyaem
        contact.text = self.text
        print 'Sent(->): ', self.text, '\n---------------------'
        #rasshifrovivaem
        contact.transcriptRSA()

