#!/usr/bin/python

engalphabet = list('abcdefghijklmnopqrstuvwxyz')

def charchange(integer):
    if integer > 10.88:
        return 'e'
    elif integer > 8.615:
        return 't'
    elif integer > 7.84:
        return 'a'
    elif integer > 7.24:
        return 'o' 
    elif integer > 6.86:
        return 'i'
    elif integer > 6.54:
        return 'n'
    elif integer > 6.21:
        return 's'
    elif integer > 6.04:
        return 'h'
    elif integer > 5.12:
        return 'r'
    elif integer > 4.14:
        return 'd'
    elif integer > 3.405:
        return 'l'
    elif integer > 2.77:
        return 'c'
    elif integer > 2.585:
        return 'u'
    elif integer > 2.385:
        return 'm'
    elif integer > 2.295:
        return 'w'
    elif integer > 2.125: 
        return 'f'
    elif integer > 1.995:
        return 'g'
    elif integer > 1.95: 
        return 'y'
    elif integer > 1.71:
        return 'p'
    elif integer > 1.235:
        return 'b'
    elif integer > 0.875:
        return 'v'
    elif integer > 0.46:
        return 'k'
    elif integer > 0.145:
        return 'x'
    elif integer > 0.12:
        return 'j'
    elif integer > 0.08:
        return 'q'
    else: 
        return 'z'

def cipher():
    stringout = ''
    file = open('input')
    for char in file.read():
        if char in engalphabet:
            if checkeng(char) > 15:
                stringout = stringout + '0'
            stringout = stringout + str(25-checkeng(char))
        else:
            stringout = stringout + char
    file.close()
    file = open('input','w')
    file.write(stringout)
    file.close
    print '--------'
    print stringout

def decipher():
    stringout = ''
    charlist = []
    chars = ''
    i = 0
    file = open('input')
    for char in file.read():
        if (char != '.') and (char != ',') and (char != ' ') and (char != '\n'):
            chars = chars + char
            if i == 1:
                charlist.append(chars)
                chars = ''
                i = -1
            i += 1
        else:
            charlist.append(char)
    file.close()
    for char in charlist:
        if (char != '.') and (char != ',') and (char != ' ') and (char != '\n'):
            stringout += charchange(charlist.count(char)*100/float(len(charlist)))
        else:
            stringout += char
    print '--------'
    print(stringout)
    file = open('input', 'w')
    file.write(stringout)
    file.close()

def readcipher():
    stringout = ''
    chars = ''
    i = 0
    file = open('input')
    for char in file.read():
        if (char != '.') and (char != ',') and (char != ' ') and (char != '\n'):
            chars = chars + char
            if i == 1:
                print chars
                stringout = stringout + engalphabet[25-int(chars)]
                i = -1
                chars = ''
            i += 1
        else:
            stringout += char
    file.close()
    file = open('input','w')
    file.write(stringout)
    file.close
    print '--------'
    print stringout

if __name__ == '__main__':
    while True:
        func = raw_input('--------\nWrite 0 to cipher text, 1 to uncipher text,2 for decipher text\nYour command: ')
        if func == '0':
                cipher()
        elif func == '1':
                readcipher()
        elif func == '2':
                decipher()
        else:
            print('There is not such command')
