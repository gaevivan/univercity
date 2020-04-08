#!/usr/bin/python

from Lexer import Lexer
from Parser import Parser
from Polizprocessor import Polizprocessor
from Token import Token

if __name__ == '__main__':
    input = open('test-valid.input')
    lexer = Lexer(input)
    parser = Parser(lexer.tokenlist)
    poliz = Polizprocessor(lexer.tokenlist)
    input.close()
    print 'Token list: ', lexer.tokenlist
    print 'AST after parser: ', parser.checksyntax()
    print 'Token list after poliz: ', poliz.getpoliz()
    print 'Variable table: ', poliz.calculatepoliz()
    print '\n...done...'
