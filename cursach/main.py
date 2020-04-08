#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, run, static_file, template, route, get, post, request, redirect
import data
import os
import sqlite3

PORT = 8008
MAX_ROWS = 8

app = Bottle()

@get('/static/css/<filepath:re:.*\.css>')
def css(filepath):
    return static_file(filepath, root='static/css')

@get('/static/font/<filepath:re:.*\.ttf>')
def font(filepath):
    return static_file(filepath, root='static/font')

@get('/static/img/<filepath:re:.*\.png>')
def img(filepath):
    return static_file(filepath, root='static/img')

@get('/static/js/<filepath:re:.*\.js>')
def js(filepath):
    return static_file(filepath, root='static/js')

@route('/', methods=['GET', 'POST']) 
@route('/index', methods=['GET', 'POST']) #при переходе на /index запускается функция index()
def index():
    rows = data.readconfig() #все редактируемые сигналы
    table = []
    for row in rows:
        table.append([row[0], row[1], row[2], row[3]])
        for item in table:
            item[1] = item[1].replace('.',' ')
    data.changebin()
    return template('index.tpl', rows=table) #вывод на экран браузера представления

@post('/reset') #обработка post-запроса на сброс всех сигналов
def reset():
    rows = data.selectAll()
    for row in rows:
        if row[3] == "Analog":
            data.changebase("0", row[0])
        else:
            data.changebase("False", row[0])
    data.changebin()

@post('/new') #обработка post-запроса на изменение сигналов
def new():
    data.changebase(request.forms.get('value'), request.forms.get('id'))
    data.changebin()

if __name__ == '__main__':
    run(port=PORT) #запуск сервераr
