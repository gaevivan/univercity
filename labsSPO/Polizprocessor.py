from Token import Token


class Polizprocessor:
    def __init__(self, tokenlist):
        self.tokenlist = tokenlist
        self.newtokenlist = []
        self.stack = []
        self.i = -1
        self.j = -1
        self.variabletable = {}

    def getnexttoken(self):
        self.i += 1
        return self.tokenlist[self.i]

    def getpoliz(self):
        while self.i < len(self.tokenlist) - 1:
            token = self.getnexttoken()
            if (token.type == 'integer' or token.type == 'variable' or token.type == 'declaration'):
                self.newtokenlist.append(token)
            elif (token.type == 'operation' or token.type == 'assignment'):
                if self.stack == []:
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
            elif token.type == 'end':
                self.stack.reverse()
                for item in self.stack:
                    self.newtokenlist.append(item)
                self.stack = []
                self.newtokenlist.append(token)
        return self.newtokenlist

    def getnextnewtoken(self):
        self.j += 1
        return self.newtokenlist[self.j]


    def calculatepoliz(self):
        while self.j < len(self.newtokenlist) - 1:
            token = self.getnextnewtoken()
            if token.type == 'declaration':
                self.variabletable[self.getnextnewtoken().value] = 0
                self.getnextnewtoken()
            elif (token.type == 'integer' or token.type == 'variable'):
                self.stack.append(token.value)
            elif (token.type == 'operation' or token.type == 'assignment'):
                a = self.stack.pop()
                b = self.stack.pop()
                c = b
                result = 0
                try:
                    a = int(a)
                except ValueError:
                    a = self.variabletable[a]
                try:
                    b = int(b)
                except ValueError:
                    b = self.variabletable[b]
                if token.value == '+':
                    result = b + a
                elif token.value == '-':
                    result = b - a
                elif token.value == '*':
                    result = b * a
                elif token.value == '/':
                    result = b / a
                elif token.value == '=':
                    result = a
                    self.variabletable[c] = a
                self.stack.append(result)
            elif token.type == 'end':
                self.stack = []
        return self.variabletable

