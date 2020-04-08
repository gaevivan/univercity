from Token import Token
import re

OPERATION = 'operation'
VARIABLE = 'variable'
END = 'end'
INTEGER = 'integer'
ASSIGNMENT = 'assignment'
DECLARATION = 'declaration'


class Lexer:
    def __init__(self, file):
        self.tokenlist = []
        for line in file:
            items = line.split(' ')
            for item in items:
                if re.match(r'var', item):
                    self.tokenlist.append(Token(DECLARATION, item))
                elif re.match(r'=', item):
                    self.tokenlist.append(Token(ASSIGNMENT, item))
                elif re.match(r'[A-Za-z][A-Za-z0-9_]*', item):
                    if re.search(r'\;', item) != None:
                        self.tokenlist.append(Token(VARIABLE, item[:-2]))
                        self.tokenlist.append(Token(END, ';'))
                    else:
                        self.tokenlist.append(Token(VARIABLE, item))
                elif (re.match(r'-', item) or re.match(r'\+', item) or re.match(r'\*', item)):
                    self.tokenlist.append(Token(OPERATION, item))
                elif re.match(r'[0-9]*', item):
                    if re.search(r'\;', item) != None:
                        self.tokenlist.append(Token(INTEGER, item[:-2]))
                        self.tokenlist.append(Token(END, ';'))
                    else:
                        self.tokenlist.append(Token(INTEGER, item))

