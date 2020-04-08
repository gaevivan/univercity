from Token import Token
import re


class Poliz:
    def __init__(self, tokenlist):
        self.tokenlist = tokenlist
        self.newtokenlist = []
        self.stack = []
        self.i = -1
        self.vartable = {}
        self.structtable = []

    def getnexttoken(self):
        self.i += 1
        return self.tokenlist[self.i]

    def getnextnewtoken(self):
        self.i += 1
        return self.newtokenlist[self.i]

    def getpoliz(self):
        while self.i < (len(self.tokenlist) - 2):
            token = self.getnexttoken()
            if token.type == 'end':
                self.stack.reverse()
                for item in self.stack:
                    self.newtokenlist.append(item)
                self.stack = []
                self.newtokenlist.append(token)
            elif token.value == '(':
                self.stack.append(token)
            elif token.value == ')':
                if self.stack != []:
                    top = self.stack.pop()
                    while top.value != '(':
                        self.newtokenlist.append(top)
                        top = self.stack.pop()
                    if self.stack[0].value == '(':
                        self.stack.pop()
            elif (token.type == 'oper' or token.type == 'assign'):
                if (token.value == '>' or token.value == '<'):
                    self.newtokenlist.append(token)
                elif self.stack == []:
                    self.stack.append(token)
                elif (token.value == '='):
                    if (self.stack[0].value == '+' or self.stack[0].value == '-' or self.stack[0].value == '*' or self.stack[0].value == '/'):
                        self.stack.reverse()
                        for item in self.stack:
                            self.newtokenlist.append(item)
                        self.stack = []
                        self.newtokenlist.append(token)
                    else:
                        self.stack.append(token)
                elif (token.value == '+' or token.value == '-'):
                    if (self.stack[0].value == '*' or self.stack[0].value == '/'):
                        self.stack.reverse()
                        for item in self.stack:
                            self.newtokenlist.append(item)
                        self.stack = []
                        self.newtokenlist.append(token)
                    else:
                        self.stack.append(token)
                else:
                    self.stack.append(token)
            else:
                self.newtokenlist.append(token)
        return self.newtokenlist

    def calcpoliz(self):
        states = []
        i = 0
        states.append([])
        self.stack = []
        self.i = -1
        curindex = 0
        curcycle = []
        while self.i < (len(self.newtokenlist) - 1):
            token = self.getnextnewtoken()
            if token.type == 'end':
                states[i].append(token)
                i += 1
                states.append([])
            else:
                states[i].append(token)
        i = -1
        while i < len(states)-1:
            i += 1
            state = states[i]
            if state[0].type == 'func':
                if state[0].value == 'incr':
                    self.vartable[state[1].value] += 1
                elif state[0].value == 'decr':
                    self.vartable[state[1].value] -= 1
                elif state[0].value == 'print':
                    if state[1].type == 'var':
                        print self.vartable[state[1].value]
                    elif state[1].type == 'int':
                        print state[1].value
            elif state[0].type == 'struct':
                self.structtable.append(state[1].value)
                for item in state:
                    if (item.type == 'var' and item.value != state[1].value):
                        self.vartable[state[1].value+'.'+item.value] = 0
            elif state[0].type == 'var':
                for item in self.structtable:
                    if re.search(r'\.', state[0].value) != None:
                        text = state[0].value.split('.')
                        if re.search(item, state[0].value) != None:
                            if text[0] != item:
                                raise Exception('Invalid struct')
                        for elem in self.vartable:
                            if self.vartable.get(state[0].value) == None:
                                raise Exception('Struct has not this arg')
                self.vartable[state[0].value] = 0
                for item in state:
                    if (item.type == 'var' or item.type == 'int'):
                        self.stack.append(item.value)
                    elif (item.type == 'oper' or item.type == 'assign'):
                        a = self.stack.pop()
                        b = self.stack.pop()
                        c = b
                        result = 0
                        try:
                            a = int(a)
                        except ValueError:
                            a = self.vartable[a]
                        try:
                            b = int(b)
                        except ValueError:
                            b = self.vartable[b]
                        if item.value == '+':
                            result = b + a
                        elif item.value == '-':
                            result = b - a
                        elif item.value == '*':
                            result = b * a
                        elif item.value == '/':
                            result = b / a
                        elif item.value == '=':
                            result = a
                            self.vartable[c] = a
                        self.stack.append(result)
                    elif item.type == 'end':
                        self.stack = []
            elif state[0].type == 'cycle':
                curindex = i
                curcycle = state
            elif state[0].type == 'block':
                if curcycle[0].value == 'for':
                    for item in curcycle:
                        if item.type == 'int':
                            item.value = int(item.value) - 1
                            if item.value == 0:
                                curindex = i
                            else:
                                i = curindex
                        elif item.type == 'var':
                            self.vartable[item.value] -= 1
                            if self.vartable[item.value] == 0:
                                curindex = i
                            else:
                                i = curindex
                if curcycle[0].value == 'while':
                    a = 0
                    b = 0
                    for item in curcycle:
                        if item.type == 'var' or item.type == 'int':
                            if item == curcycle[1]:
                                a = self.vartable[item.value]
                            else:
                                b = item.value
                        elif item.type == 'oper':
                            if item.value == '>':
                                if a > b:
                                    i = curindex
                                else:
                                    curindex = i
                            else:
                                if a < b:
                                    i = curindex
                                else:
                                    curindex = i