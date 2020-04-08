from Token import Token
import re


class Lexer:
    def __init__(self, file):
        self.tokenlist = []
        for line in file:
            items = line.split(' ')
            for item in items:
                if (re.match(r'while', item) or re.match(r'for', item)):
                    self.tokenlist.append(Token('cycle', item))
                elif re.match(r'struct', item):
                    self.tokenlist.append(Token('struct', item))
                elif re.match(r',', item):
                    self.tokenlist.append(Token('comma', item))
                elif re.match(r':', item):
                    self.tokenlist.append(Token('doubledot', item))
                elif (re.match(r'\{', item) or re.match(r'\}', item)):
                    if re.search(r'\n', item) != None:
                        self.tokenlist.append(Token('block', item[:-1]))
                        self.tokenlist.append(Token('end', '\n'))
                    else:
                        self.tokenlist.append(Token('block', item))
                elif (re.match(r'\(', item) or re.match(r'\)', item)):
                    if re.search(r'\n', item) != None:
                        self.tokenlist.append(Token('bracket', item[:-1]))
                        self.tokenlist.append(Token('end', '\n'))
                    else:
                        self.tokenlist.append(Token('bracket', item))
                elif (re.match(r'incr', item) or re.match(r'decr', item) or re.match(r'print', item)):
                    self.tokenlist.append(Token('func', item))
                elif re.match(r'=', item):
                    self.tokenlist.append(Token('assign', item))
                elif (re.match(r'<', item) or re.match(r'>', item) or re.match(r'-', item) or re.match(r'\+', item) or re.match(r'\*', item) or re.match(r'/', item)):
                    self.tokenlist.append(Token('oper', item))
                elif re.match(r'[A-Za-z][A-Za-z0-9_]*', item):
                    if re.search(r'\n', item) != None:
                        self.tokenlist.append(Token('var', item[:-1]))
                        self.tokenlist.append(Token('end', '\n'))
                    else:
                        self.tokenlist.append(Token('var', item))
                elif re.match(r'[0-9]*', item):
                    if re.search(r'\n', item) != None:
                        self.tokenlist.append(Token('int', item[:-1]))
                        self.tokenlist.append(Token('end', '\n'))
                    else:
                        self.tokenlist.append(Token('int', item))
