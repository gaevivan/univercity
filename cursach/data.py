#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import *
import sqlite3
import os
import fnmatch

INTEGER_BINARY_LENGTH = 32
FLOAT_BINARY_LENGTH = 64
BASE_NAME = 'data.db'

def connectDB(query, type=False): #main db-func
    connection = sqlite3.connect(BASE_NAME) #подключение к бд
    cursor = connection.cursor()
    cursor.execute(query) #составление запроса
    connection.commit() #выполнение запроса
    if type: #в зависимости от параметра типа
        result = cursor.fetchall() #запросить все данные
    else:
        result = cursor.fetchone() #запросить строчку
    cursor.close()
    connection.close()
    return result #функция возвращает результат запроса

def changebin(): #сохранения значений базы в бинарниках
    query = 'SELECT * FROM signals' #стандартный запрос
    value = connectDB(query, True)
    bin_data = ['','',[]] #name,type,data
    for item in os.listdir(os.getcwd()):
        if fnmatch.fnmatch(item, '*.bin'):
            os.remove(item)
    for item in value: #проходит все значения базы данных
        if item == value[0]: #самое первое значение
            if item[2] == 'True':
                bin_data[1] = 'digital'
            elif item[2] == 'False':
                bin_data[1] = 'digital'
            else:
                bin_data[1] = 'analog'
            bin_data[0] = item[1].split('.')[0]
            if item[2] == 'True':
                bin_data[2].append(1)
            elif item[2] == 'False':
                bin_data[2].append(0)
            else:
                bin_data[2].append(item[2])
        elif item[0] == 0: #первое значение каждого модуля
            with open(os.path.join(item[1].split('.')[0]) + '.bin', 'wb') as f:
                if bin_data[1] == 'digital':
                    f.write(pack('32b', *bin_data[2]))
                elif bin_data[1] == 'analog':
                    for datas in bin_data[2]:
                        f.write(pack('h', datas))
            if item[2] == 'True':
                bin_data[1] = 'digital'
            elif item[2] == 'False':
                bin_data[1] = 'digital'
            else:
                bin_data[1] = 'analog'
            bin_data[0] = item[1].split('.')[0]
            bin_data[2].clear()
            if item[2] == 'True':
                bin_data[2].append(1)
            elif item[2] == 'False':
                bin_data[2].append(0)
            else:
                bin_data[2].append(item[2])
        elif item[0] == (len(value) - 1): #последнее значение базы данных
            if item[2] == 'True':
                bin_data[2].append(1)
            elif item[2] == 'False':
                bin_data[2].append(0)
            else:
                bin_data[2].append(item[2])
            with open(os.path.join(item[1].split('.')[0]) + '.bin', 'wb') as f:
                if bin_data[1] == 'digital':
                    print(*bin_data[2])
                    f.write(pack('32b', *bin_data[2]))
                elif bin_data[1] == 'analog':
                    for datas in bin_data[2]:
                        f.write(pack('h', int(datas)))
        else: #очередное значение, не первое в базе или модуле и не последнее
            if item[2] == 'True':
                bin_data[2].append(1)
            elif item[2] == 'False':
                bin_data[2].append(0)
            else:
                bin_data[2].append(item[2])

def changebase(number, id): #меняет значение одного сигнала в базе по айди
    if number:
        connectDB('UPDATE signals SET value="'+str(number)+'" WHERE id='+str(id))

def selectAll(): #возвращает данные по всем сигналам в базе
    value = connectDB('SELECT * FROM signals', True)
    return value

def readconfig(): #читает конфигурационный файл, обнуляет базу данных, заносит туда пустые значения
    f = open('emulator_config_file.cfg', 'r')
    data = connectDB('SELECT * FROM signals', True)
    l = [] #список для данных одного модуля
    count = 0 #количество всех сигналов всех модулей в сумме
    id_counter = 0 #идентификатор сигналов в рамках одного модуля
    for line in f:
        l.append(line.split())
        count = count + int(line.split()[2])
        stop = False
        for item in data: #проверка наличия изменений в модулях
            if item[1] != line.split()[0]:
                stop = True
    if stop: #если изменился состав модулей, то чистит базу и заполняет пустыми значениями
        connectDB('DELETE FROM signals', True)
        for item in l:
            element = ['','','']
            if item[1] == 'ai':
                element[1] = 'Analog'
                element[2] = '0'
            else:
                element[1] = 'Digital'
                element[2] = 'False'
            for value in range(int(item[2])):
                connectDB('INSERT INTO signals(id,name,value,type) VALUES('+str(id_counter)+',"'+item[0]+'.'+str(value)+'","'+element[2]+'","'+element[1]+'")')
                id_counter += 1
    f.close
    return data
