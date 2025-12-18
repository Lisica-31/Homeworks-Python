f = open ('web_clients_correct.csv', 'r', encoding = 'utf-8')

lines = f.readline()
f_title = lines[0]
f_line = lines[1:]

class Web_Client:
    def __init__ (self, name, device_type, browser, sex, age, bill, region):
        self.name = name
        self.device_type = device_type
        self.browser = browser
        self.sex = sex
        self.age = age
        self.bill = bill
        self.region = region
 
    device_type_part = {
        'mobile': 'мобильного устройства',
        'desktop': 'компьютера',
        'laptop': 'ноутбока',
        'tablet': 'планшета',
    }
    sex_part = {
        'female': 'женского пола',
        'male': 'мужского пола'
    }
    sex_part_verb = {
        'female': 'совершила',
        'male': 'совершил'
    }

    def message (self):
        message = (f"Пользователь {self.name} {self.sex_part[self.sex]}, {self.age} лет {self.sex_part_verb[self.sex]}" 
                   f"покупку на {self.bill} у.е. с {self.device_type_part[self.device_type]}, браузера {self.browser}. ")
        if self.region != '-':
            message += (f"Регион, из которого совершалась покупка: {self.region}")
        return message


def split (line):
    return f_line.split(',')

def web_client_from_line (line):
    parts = split (line)
    return Web_Client (name=parts[0].strip(),
                       device_type=parts[1].strip(),
                       browser=parts[2].strip(),
                       sex=parts[3].strip(),
                       age=parts[4].strip(),
                       bill=parts[5].strip(),
                       region=parts[6].strip()
                       )

web_clients =[]
for f_line in f:
    web_client = web_client_from_line(f_line)
    web_clients.append(web_client)

f.close()

output_f = open('web_clients_message.txt', 'w', encoding = 'utf-8')

for client in web_clients:
    message = client.message()
    output_f.write (message + '\n')

output_f.close()
