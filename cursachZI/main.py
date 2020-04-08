#!/usr/bin/python

from Base import Base
from Encrypt import Contact
from Quarantine import Quarantine

if __name__ == '__main__':
    login = ''
    db = Base('data.db')
    line = '-----------------------------------------'
    db.makedefault()
    print '\nCommands: \nload - to connect and load, \nbreak - to break connection, \nsend - to send data, \nshow - show data'
    while True:
        command = raw_input('\n')
        if command == 'load':
            if login == '':
                print line
                login = raw_input('Enter login: ')
                password = raw_input('Enter password: ')
                password2 = raw_input('Verify password: ')
                if password != password2 :
                    print '\n!!!Error!!!\nDifferent passwords...\n'
                    login = ''
                else:
                    if db.checkpassword(login, password, password2):
                        text = db.gettext(login)
                        loadtext = text.split()
                        loader = Quarantine(loadtext)
                        loader.start()
                        while loader.outtext == '':
                            pass
                        current = Contact(loader.outtext, 0)
                        if loader.outtext == 'Failed':
                            login = ''
                            print 'Data ', loader.outtext, '\n', line
                    else:
                        login = ''
            else:
                print '\n!!!Error!!!\nYou need to break connection\n'
        elif command == 'break':
            if login == '':
                print '\n!!!Error!!!\nYou need to create connection for break!'
            else:
                print line, '\nConnection lost...\n', line, '\n'
                login = ''
                password = ''
                password2 = ''
                contact = ''
        elif command == 'send': 
            if login != '':
                print line
                contact = raw_input('Enter destination: ')
                if db.checkcontact(contact):
                    to = Contact('', 1)
                    current.getkey(to)
                    current.send(to)
                    db.save(contact, to.text)
                    print '\n', line
                else:
                    print '\n!!!Error!!!\nDestination isnt exists'
            else:
                print '\n!!!Error!!!\nYou need to create connection or to have some text in current contact'
        elif command == 'show':
            if login != '':
                print line, '\nLogin: ', login, '\nText: ', current.text, '\n', line, '\n'
            else:
                print '\n!!!Error!!!\nYou need to create connection for show!'
        else:
            print '\n!!!Error!!!\nThere isnt such command, try again'
