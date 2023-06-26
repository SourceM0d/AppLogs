import re
import sqlite3
import easygui
import tkinter as tk
from datetime import datetime

File = easygui.fileopenbox(filetypes=["*.log"],title='Путь к файлу логов')

# Шаблон регулярного выражения для парсинга логов Apache
pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\S+)'

def parse_log_line(line):
    """
    Функция для парсинга строки лога Apache
    """
    match = re.match(pattern, line)
    if match:
        return {
            'remote_host': match.group(1),
            'remote_user': match.group(2),
            'time': match.group(4),
            'method': match.group(5),
            'url': match.group(6),
            'protocol': match.group(7),
            'status': match.group(8),
            'size': match.group(9)
        }
    else:
        return None

# Создаем соединение с БД
conn = sqlite3.connect('logs.db')
cur = conn.cursor()

# Создаем таблицу для хранения логов
try:
    sq = cur.execute('SELECT * FROM logs')
    if (sq):
        print('Таблица уже была создана')
except:
    conn.execute('''CREATE TABLE IF NOT EXISTS logs
                        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        remote_host TEXT NULL,
                        remote_user TEXT NULL,
                        time TEXT NULL,
                        method TEXT NULL,
                        url TEXT NULL,
                        protocol TEXT NULL,
                        status INTEGER NULL,
                        size INTEGER NULL);''')
    print('Table create')

cur.execute("SELECT MAX(ID) FROM logs")
max_id = cur.fetchone()
max_id = str(max_id).replace(',','')
max_id = max_id.replace('(','')
max_id = max_id.replace(')','')


# Открываем файл с логами Apache
def open_log(x):
    i = 0
    with open(f'{x}', 'r') as f:
        for line in f:
            try:
                cur.execute("SELECT MAX(ID) FROM logs")
                max_id = cur.fetchone()
                max_id = str(max_id).replace(',', '')
                max_id = max_id.replace('(', '')
                max_id = max_id.replace(')', '')
                max_id = int(max_id)
                if (max_id):
                    if(i < max_id):
                        # print(f'Строка {i} не может быть внесена так как меньше последней строки в таблице {max_id}')
                        i = i + 1
                    elif(i >= max_id):
                        # Парсим строку лога
                        log_data = parse_log_line(line)
                        timestamp_format = '%d/%b/%Y:%H:%M:%S %z'
                        parsed_timestamp = datetime.strptime(log_data['time'], timestamp_format)
                        # cc = str(parsed_timestamp).split(' ',1)
                        # date = cc[0]
                        # cc2 = cc[1].split('-',1)
                        # timezone = cc2[1]
                        # time3 = cc2[0]
                        if log_data:
                            # Записываем лог в БД
                            cur.execute('''INSERT INTO logs (remote_host, remote_user, time, method, url, protocol, status, size)
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                        (log_data['remote_host'], log_data['remote_user'],parsed_timestamp, log_data['method'],
                                         log_data['url'], log_data['protocol'], log_data['status'], log_data['size']))
                            conn.commit()
                        i = i + 1
            except:
                # Парсим строку лога
                log_data = parse_log_line(line)
                timestamp_format = '%d/%b/%Y:%H:%M:%S %z'
                parsed_timestamp = datetime.strptime(log_data['time'], timestamp_format)
                # cc = str(parsed_timestamp).split(' ',1)
                # date = cc[0]
                # cc2 = cc[1].split('-',1)
                # timezone = cc2[1]
                # time3 = cc2[0]
                if log_data:
                    # Записываем лог в БД
                    cur.execute('''INSERT INTO logs (remote_host, remote_user, time, method, url, protocol, status, size)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                (log_data['remote_host'], log_data['remote_user'], parsed_timestamp, log_data['method'],
                                 log_data['url'], log_data['protocol'], log_data['status'], log_data['size']))
                    conn.commit()



if File:
    open_log(File)
    print('Успешно')
else:
    print('Не выбран путь к логам!')