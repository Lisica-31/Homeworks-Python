from datetime import datetime

newspapers_formats = {
    'The Moscow Times': ['Wednesday, October 2, 2002', '%A, %B %d, %Y'],
    'The Guardian':['Friday, 11.10.13', '%A, %d.%m.%y'],
    'Daily News':['Thursday, 18 August 1977','%A, %d %B %Y'] 
}

while True:
    user_input = input('Введите название газеты или end для завершения: ')
    if user_input == 'end':
        break
    try:    # ИЛИ if user_input in newspapers_formats.keys():
        print (datetime.strptime(newspapers_formats[user_input][0], newspapers_formats[user_input][1]))
    except:
        print('Этой газеты нет')
