from Token import Token


class AST(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __str__(self):
        return '({value}, {children})'.format(
            value=repr(self.value),
            children=repr(self.children)
        )

    def __repr__(self):
        return self.__str__()

class Parser:
    def __init__(self, tokenlist):
        self.treelist = []
        self.variabletable = []
        self.i = -1
        self.tokenlist = tokenlist

    def getnexttoken(self):
        self.i += 1
        return self.tokenlist[self.i]

    def checksyntax(self):
        token = Token('', '')
        while self.i < len(self.tokenlist) - 2:
            token = self.getnexttoken()
            if token.type == 'declaration':
                self.treelist.append(AST(token.type, [token.value, self.variable(), self.end()]))
            else:
                self.treelist.append(AST(self.assignment(), [token.value, self.expression(), ';']))
        return AST('program', self.treelist)

    def variable(self):
        token = self.getnexttoken()
        if token.type == 'variable':
            self.variabletable.append(token.value)
            return token.value
        else:
            raise Exception('Invalid syntax 95')

    def end(self):
        token = self.getnexttoken()
        if token.type == 'end':
            return token.value
        else:
            raise Exception('Invalid syntax 101')

    def assignment(self):
        token = self.getnexttoken()
        if token.type == 'assignment':
            return token.value
        else:
            raise Exception('Invalid syntax 107')

    def expression(self):
        token = self.getnexttoken()
        if (token.type == 'variable' or token.type == 'integer'):
            a = 0
            for item in self.variabletable:
                if item == token.value:
                    a = 1
            if (a == 0 and token.type == 'variable'):
                raise Exception('Declaration error')
            nexttoken = self.getnexttoken()
            if nexttoken.type == 'end':
                return token.value
            elif nexttoken.type == 'operation':
                return AST(nexttoken.value, [
                    token.value,
                    self.expression()
                ])
            else:
                raise Exception('Invalid syntax 120')
        else:
            raise Exception('Invalid syntax 122')


