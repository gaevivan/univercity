import hashlib
import sqlite3


class Base:
    def __init__(self, name):
        self.name = name

    def gettext(self, login):
        connection = sqlite3.connect(self.name)
        cur = connection.cursor()
        cur.execute("SELECT value from auth WHERE login = '"+login+"'")
        return cur.fetchone()[0]

    def makedefault(self):
        connection = sqlite3.connect(self.name)
        cur = connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS auth(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, hashpass TEXT NOT NULL, salt TEXT NOT NULL, value TEXT NOT NULL);")
        connection.commit()
        cur.execute("INSERT INTO auth(login, hashpass, salt, value) VALUES ('ivgaev', 'a7ad174f336ab0fb7da10bd77c56a743368a9e3cd7742043434a62bc9c7c961e', '1SEPTEMBER2016', '%&MOSCOW IS &%THE BEST CITY ALL OF THE WORLD');")
        #cur.execute("INSERT INTO auth(login, hashpass, salt, value) VALUES ('idrozdov', 'a7ad174f336ab0fb7da10bd77c56a73368a9e3cd7742043434a62bc9c7c961e', '1SEPTEMBER2016', '%&URAL IS &%THE BEST CITY');")
        cur.execute("INSERT INTO auth(login, hashpass, salt, value) VALUES ('svoronkov', 'a48536b0266a7e295366a271b3636d729a44b11cfa70213a10b3c31f5fb61b71', '2SEPTEMBER2016', '**PETER IS MUCH MUCH BETTER THAN %@ MOSCOW');")
        cur.close()
        connection.commit() #PASSWORDS: ivgaev - moscow, svoronkov - peter
        connection.close()

    def checkpassword(self, login, password, password2):
        connection = sqlite3.connect(self.name)
        cur = connection.cursor()
        cur.execute("SELECT * from auth WHERE login = '"+login+"'")
        hash = hashlib.sha256()
        try:
            hash.update(password + cur.fetchone()[3])
            #cur.execute("SELECT hashpass FROM auth WHERE login = '"+login+"'")
            if hash.hexdigest() == cur.fetchone()[2]:
                return True
            else:
                print '\nWrong login or password!\n'
                return False
        except TypeError:
            print '\nWrong login or password!\n'
            return False
        cur.close()
        connection.close()

    def checkcontact(self, contact):
        connection = sqlite3.connect(self.name)
        cur = connection.cursor()
        cur.execute("SELECT login from auth WHERE login = '"+contact+"'")
        try:
            if cur.fetchone()[0] == contact:
                return True
            else:
                return False
        except TypeError:
            return False
        cur.close()
        connection.close()

    def save(self, contact, text):
        connection = sqlite3.connect(self.name)
        cur = connection.cursor()
        cur.execute("UPDATE auth SET value='"+text+"' WHERE login = '"+contact+"'")
        cur.close()
        connection.commit()
        connection.close()
        print 'Data sent and updated'
