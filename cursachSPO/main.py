#!/usr/bin/python

from Lexer import Lexer
from Parser import Parser
from Poliz import Poliz
from Token import Token

if __name__ == '__main__':
    input = open('inputcode')
    lexer = Lexer(input)
    parser = Parser(lexer.tokenlist)
    poliz = Poliz(lexer.tokenlist)
    input.close()
    parser.checksyntax()
    poliz.getpoliz()
    poliz.calcpoliz()
