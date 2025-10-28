directories = {
 '1': ['2207 876234', '11-2'],
 '2': ['10006'],
 '3': []
}


def helper(s):
    for place, num in directories.items():
        if s in num:
            return place
        
def command_s():
    s = input('Введите номер документа:\n')
    place = helper(s)
    if place:
        print ('Документ хранится на полке:\n', place)
    else:
        print ('Документ хранится на полке:\n Документ не найден')


while True:
    command = input ('Введите команду:\n')
    if command == 's':
        command_s()
    else:
        break
