def hash(secondname):
    return len(secondname)

class HashMap:
    def __init__():
        hmap = array()
        for i in range(20):
            hmap.append(array())
    def add(firstname, secondname):
        bucket = (hash(secondname)+20)%20
        hmap[bucket].append(secondname)
        hmap[bucket].append(firstname)
    def get(secondname):
        bucket = (hash(secondname)+20)%20
        return hmap[bucket][hmap[bucket].index(secondname)+1]
        
#Ключ - фамилия, данные - имя. Функция get - возвращает имя по фамилии, функция add - добавляет имя и фамилию в HashMap
#Расчитано на максимум 20-ти символьную фамилию. Хэш-функция возвращает просто длину фамилии
