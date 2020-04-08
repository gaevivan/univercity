import hashlib
import sqlite3

def makebase():
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS auth(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, hashpass TEXT NOT NULL, salt TEXT NOT NULL);")
    connection.commit()
    cur.execute("INSERT INTO auth(login, hashpass, salt) VALUES ('ivgaev', '877a9fae4361069d9a7577e91c8db5a7f7dd6e5c69a36c9cb9d59fecac81d18e', '1SEPTEMBER2016');")
    cur.close()
    connection.commit()
    connection.close()
    
def checkpassword(login, password, password2):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM auth WHERE login = '"+login+"'")
    hash = hashlib.sha256()
    hash.update(password + cur.fetchone()[3])
    cur.execute("SELECT hashpass FROM auth WHERE login = '"+login+"'")
    if hash.hexdigest() == cur.fetchone()[0]:
        return '\nRight password!\n'
    else:
        return '\nWrong login or password!\n'
    cur.close()
    connection.close()
    
if __name__ == '__main__':
    makebase()
    while True:
        login = raw_input('Enter login: ')
        password = raw_input('Enter password: ')
        password2 = raw_input('Verify password: ')
        if password != password2 :
            print '\n!!!Error!!!\nDifferent passwords...\n'
        else:
            print checkpassword(login, password, password2)
