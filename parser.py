import os
import csv
from glob import glob

class MessageAndroid:
    def __init__(self, raw_message):
        self.raw_message = raw_message
    
    @property
    def date(self):
        return self.raw_message[:10]
    
    @property
    def hour(self):
        return self.raw_message[11:16]
    
    @property
    def number_raw(self):
        number = self.raw_message.split(' - ‎')
        number = number[1][:17]
        number = number.strip()
        return number
    
    @property
    def number(self):
        number = self.number_raw.replace('+', '')
        number = number.replace(' ', '')
        number = number.replace('-', '')
        number = number.strip()

        return number
    
    @property
    def message(self):
        message = self.raw_message.split(self.number_raw)
        message = message[1].strip()
        return message
    
    @property
    def is_joined(self):
        if 'entrou' in self.message:
            return True
        return False
    
    @property
    def is_left(self):
        if 'saiu' in self.message:
            return True
        return False


def _load_chat_from_android(filename):
    strings_to_identify = ['entrou usando', 'saiu']
    
    with open(filename) as handle:
        data = handle.read()
    
    messages = []
    for message in data.split('\n'):
        for string in strings_to_identify:
            if string in message:
                messages.append(MessageAndroid(message))
    
    return messages


def _generate_report_data_from_android(directory):
    numbers = {}

    for filename in glob(f'{directory}/*.txt'):
        for message in _load_chat_from_android(filename):
            if message.is_joined:
                numbers[message.number] = {
                    'number': message.number,
                    'date_joined': message.date,
                    'hour_joined': message.hour,
                    'date_left': None,
                    'hour_left': None,
                }
        
            if message.is_left:
                numbers[message.number]['date_left'] = message.date
                numbers[message.number]['hour_left'] = message.hour
    
    return [data for number, data in numbers.items()]


def generate_report_from_android(directory):
    with open(os.path.join(directory, '00numbers.csv'), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        
        spamwriter.writerow(
            [
                'Número', 
                'Data de Entrada', 
                'Hora de Entrada', 
                'Data de Saída',
                'Hora de Saída',
                'Link p/ Contato',
            ]
        )
        
        for values in _generate_report_data_from_android(directory):
            spamwriter.writerow(
                [
                    values['number'],
                    values['date_joined'],
                    values['hour_joined'],
                    values['date_left'],
                    values['hour_left'],
                    f"https://wa.me/{values['number']}",
                ]
            )

