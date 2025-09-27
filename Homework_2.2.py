boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

#boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']
#girls = ['Kate', 'Liza', 'Kira', 'Emma',  'Trisha']

if len(boys) == len(girls):
    print ('Идеальные пары: ')
    for i in range (len(boys)):
        boys, girls = sorted(boys), sorted(girls)
        print (str(boys[i]) + ' и ' + str(girls[i]))
else:
    print ('Внимание, кто-то может остаться без пары! ╰(°〇°)╯')
