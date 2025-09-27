word = input('Введите слово из латинских букв: ' )
index = int(len(word) / 2)
if len(word) % 2 == 0:
    print (word[index-1:index+1])
else:
    print (word[index])
