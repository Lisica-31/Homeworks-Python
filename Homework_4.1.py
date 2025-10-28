documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]


def helper(person):
    for num in documents:
        if num['number'] == person:
            return num['name']
        
def command_p():
    person = helper(input('Введите номер документа:\n'))
    if person:
        print ('Владелец документа:\n', person)
    else:
        print ('Владелец документа:\n Владелец не найден')
            

while True:
    command = input ('Введите команду:\n')
    if command == 'p':
        command_p ()
    else:
        break
