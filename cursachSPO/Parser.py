from Token import Token

class Parser:
    def __init__(self, tokenlist):
        self.i = -1
        self.tokenlist = tokenlist

    def getnexttoken(self):
        self.i += 1
        return self.tokenlist[self.i]

    def statement(self, sublist):
        nexttoken = Token('', '')
        while self.i < (len(self.tokenlist)-2):
            token = self.getnexttoken()
            if token.type == 'cycle':
                self.cycle()
            elif token.type == 'struct':
                self.struct()
            elif token.type == 'func':
                nexttoken = self.getnexttoken()
                if (nexttoken.type == 'var' or nexttoken.type == 'int'):
                    if self.getnexttoken().type != 'end':
                        raise Exception('syntax error - end of func')
                else:
                    raise Exception('syntax error - invalid func')
            elif token.type == 'var':
                nexttoken = self.getnexttoken()
                if nexttoken.type == 'assign':
                    self.expr()
                else:
                    raise Exception('syntax error - should be assign')

    def struct(self):
        nexttoken = Token('', '')
        token = self.getnexttoken()
        if token.type == 'var':
            nexttoken = self.getnexttoken()
            if nexttoken.value == ':':
                nexttoken = self.getnexttoken()
                last = Token('None', 'None')
                while nexttoken.type != 'end':
                    if (nexttoken.type == 'var' or nexttoken.type == 'comma'):
                        if (last.type == 'None' and nexttoken.type != 'var'):
                            raise Exception('Syntax error - need a variable inside struct')
                        elif (last.type == 'var' and nexttoken.type == 'var'):
                            raise Exception('Syntax error - need a comma after var inside struct')
                        elif (last.type == 'comma' and nexttoken.type == 'comma'):
                            raise Exception('Syntax error - need a var after comma inside struct')
                        last = nexttoken
                        nexttoken = self.getnexttoken()
                    else:
                        Exception('Syntax error - should be var or comma')
            else:
                raise Exception('Syntax error - struct doubledot')
        else:
            raise Exception('Syntax error - struct name')

    def expr(self):
        nexttoken = Token('', '')
        token = self.getnexttoken()
        if (token.type == 'var' or token.type == 'int'):
            nexttoken = self.getnexttoken()
            if nexttoken.type == 'oper':
                self.expr()
            elif nexttoken.type != 'end':
                raise Exception('syntax error - should be end')

    def cycle(self):
        nexttoken = Token ('', '')
        addlist = []
        if self.tokenlist[self.i].value == 'while':
            token = self.getnexttoken()
            if (token.type == 'var' or token.type == 'int'):
                if self.getnexttoken().type == 'oper':
                    nexttoken = self.getnexttoken()
                    if (nexttoken.type == 'var' or nexttoken.type == 'int'):
                        if self.getnexttoken().value == '{':
                            if self.getnexttoken().type != 'end':
                                raise Exception('syntax error - end')
                            else:
                                addlist = self.adding()
                                self.statement(addlist)
                        else:
                            raise Exception('syntax error - block')
                    else:
                        raise Exception('syntax error - var or int')
                else:
                    raise Exception('syntax error - oper')
            else:
                raise Exception('syntax error - cycle error')
        elif self.tokenlist[self.i].value == 'for':
            token = self.getnexttoken()
            if (token.type == 'var' or token.type == 'int'):
                if self.getnexttoken().value == '{':
                    if self.getnexttoken().type != 'end':
                        raise Exception('syntax error - end')
                    else:
                        addlist = self.adding()
                        self.statement(addlist)
                else:
                    raise Exception('syntax error - block')
            else:
                raise Exception('syntax error - var or int')

    def adding(self):
        result = []
        token = self.getnexttoken()
        while token.value != '}':
            result.append(token)
            token = self.getnexttoken()
        return result

    def checksyntax(self):
        self.statement(self.tokenlist)
        return 'All right...'



