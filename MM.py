import tkinter as tk
import ttkbootstrap as ttk
from tkinter import *
import pandas as pd
import sqlite3
import os
from numpy import unique


def logs_discharge():
    os.system('python Parser.py')

def authenticate(user, password):
    # Подключение к базе данных
    connect = sqlite3.connect('Customers.db')

    # Получение курсора для выполнения запросов
    cur = connect.cursor()

    # Выполнение запроса для получения пользователя
    cur.execute("SELECT * FROM customers WHERE login=? AND pass=?", (user, password))
    personal = cur.fetchone()

    # Закрытие соединения с базой данных
    cur.close()
    connect.close()

    # Если пользователь найден, возвращаем его данные
    if personal:
        return {
            "Id": personal[0],
            "Login": personal[1],
            "Password": personal[2]
        }

    # Иначе возвращаем None
    return None

def log():
    # Получение введенных пользователем данных
    username = entry_username.get()
    password = entry_password.get()

    # Аутентификация пользователя
    people = authenticate(username, password)

    if people:
        def all_param():
            def logs_all():
                connect = sqlite3.connect('logs.db')
                cursor = connect.cursor()

                window_view_logs = tk.Toplevel()
                window_view_logs.title('Логи Apache')
                window_view_logs.resizable(False, False)

                columns = ['Номер лога', 'IP','Пользователь','Время', 'Метод запроса', 'Ссылка запроса', 'Протокол запроса','Статус', 'Размер']
                tree = ttk.Treeview(window_view_logs, columns=columns, show='headings')
                tree.pack(pady=10, padx=10)

                for a in columns:
                    tree.heading(a, text=a)

                cursor.execute("SELECT * FROM logs")
                value_logs = cursor.fetchall()

                for value in value_logs:
                    tree.insert('', tk.END, values=value)

                button_view_dest = tk.Button(window_view_logs, text="Выйти", command=window_view_logs.destroy)
                button_view_dest.pack()

            def to_search_data():
                def search_from_data():
                    window_view_logs_data = tk.Toplevel()
                    window_view_logs_data.title('Логи Apache по Дате')
                    window_view_logs_data.resizable(False, False)

                    clic = sqlite3.connect('logs.db')
                    cor = clic.cursor()

                    columns = ['Номер лога', 'IP','Пользователь','Время', 'Метод запроса', 'Ссылка запроса', 'Протокол запроса','Статус', 'Размер']
                    tree = ttk.Treeview(window_view_logs_data, columns=columns, show='headings')
                    tree.pack(pady=10, padx=10)

                    for a in columns:
                        tree.heading(a, text=a)

                    cor.execute(f'select * from logs where time > "{combo_time.get()}"')
                    valueser = cor.fetchall()

                    for value in valueser:
                        tree.insert('', tk.END, values=value)

                    button_view_dest1 = tk.Button(window_view_logs_data, text="Выйти",command=window_view_logs_data.destroy)
                    button_view_dest1.pack()


                search_window_data = tk.Toplevel()
                search_window_data.geometry('300x150')
                search_window_data.resizable(False, False)
                search_window_data.title('Поиск по Дате')

                connect = sqlite3.connect('logs.db')
                cursor = connect.cursor()

                cursor.execute("Select time From logs")
                time_all = cursor.fetchall()
                time_unique_all = unique(time_all)
                time = []
                for i in time_unique_all:
                    time.append(i)
                cursor.close()

                label_time = tk.Label(search_window_data, text='Выберите время:')
                label_time.pack(pady=5, padx=5)

                combo_time = ttk.Combobox(search_window_data, values=time)
                combo_time.pack(padx=5)

                button_time = tk.Button(search_window_data, text="Посмотреть по времени", command=search_from_data)
                button_time.pack(pady=5, padx=5)

                buttons_it = tk.Button(search_window_data, text='Выход', command=search_window_data.destroy)
                buttons_it.pack(side='bottom')

            def to_search_ip():
                def search_from_ip():
                    window_view_logs_ip = tk.Toplevel()
                    window_view_logs_ip.title('Логи Apache по IP')
                    window_view_logs_ip.resizable(False, False)

                    clic = sqlite3.connect('logs.db')
                    cor = clic.cursor()

                    columns = ['Номер лога', 'IP','Пользователь','Время', 'Метод запроса', 'Ссылка запроса', 'Протокол запроса','Статус', 'Размер']
                    tree = ttk.Treeview(window_view_logs_ip, columns=columns, show='headings')
                    tree.pack(pady=10, padx=10)

                    for a in columns:
                        tree.heading(a, text=a)

                    cor.execute(f'select * from logs where remote_host = "{combo_ip.get()}"')
                    valueser = cor.fetchall()

                    for value in valueser:
                        tree.insert('', tk.END, values=value)

                    button_view_dest1 = tk.Button(window_view_logs_ip, text="Выйти",command=window_view_logs_ip.destroy)
                    button_view_dest1.pack()


                search_window_ip = tk.Toplevel()
                search_window_ip.geometry('200x150')
                search_window_ip.resizable(False,False)
                search_window_ip.title('Поиск по IP')

                connect = sqlite3.connect('logs.db')
                cursor = connect.cursor()

                cursor.execute("Select remote_host From logs")
                ip_all = cursor.fetchall()
                ip_unique = unique(ip_all)
                ip = []
                for i in ip_unique:
                    ip.append(i)
                cursor.close()

                label_ip = tk.Label(search_window_ip, text='Выберите IP:')
                label_ip.pack(anchor='nw', pady=5, padx=5)

                combo_ip = ttk.Combobox(search_window_ip, values=ip)
                combo_ip.pack(anchor='nw', padx=5)

                button_ip = tk.Button(search_window_ip, text="Посмотреть по IP", command=search_from_ip)
                button_ip.pack(anchor='nw', pady=5, padx=5)

                buttons_it = tk.Button(search_window_ip, text='Выход', command=search_window_ip.destroy)
                buttons_it.pack(side='bottom')


            window_param = tk.Toplevel()
            window_param.geometry('300x100')
            window_param.title('Вывод логов')
            window_param.resizable(False, False)

            Frames = tk.Frame(window_param)
            Frames.pack(side='top')

            button_ips = tk.Button(Frames,text="Логи по IP",command=to_search_ip).grid(row=0,column=0,pady=5,padx=5)

            button_all = tk.Button(Frames,text="Логи",command=logs_all).grid(row=0,column=1,pady=5,padx=5)

            button_dates = tk.Button(Frames,text="Логи по Дате",command=to_search_data).grid(row=0,column=2,pady=5,padx=5)

            button_it = tk.Button(window_param,text='Выход',command=window_param.destroy)
            button_it.pack(side='bottom')

        window = tk.Toplevel()
        window.geometry('300x150')
        window.title('Работа с логами')
        window.resizable(False,False)

        Frame = tk.Frame(window)
        Frame.pack(side='bottom')

        label_cust = tk.Label(window,text=f'Пользователь {username} привет!')
        label_cust.pack(pady=5)

        button_exit = tk.Button(window,text='Выйти',command=window.destroy)
        button_exit.pack(pady=10)

        button_view_logs = tk.Button(Frame,text='Посмотреть логи',command=all_param).grid(row=0,column=0,pady=10,padx=5)

        button_logs = tk.Button(Frame, text='Выгрузить логи в БД', command=logs_discharge).grid(row=0, column=1,pady=10, padx=5)

        label_error.config(text='')

    else:
        label_error.config(text=f'Пользователь {username} не найден\n'
                                f'либо введён неверный пароль.')


    entry_username.delete(0,tk.END)
    entry_password.delete(0,tk.END)

root = tk.Tk()
root.geometry('300x150')
root.title("Авторизация")
root.resizable(False, False)

# Создание виджетов для ввода имени пользователя и пароля
label_username = tk.Label(root, text="Логин пользователя:")
label_username.pack()

entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Пароль:")
label_password.pack()

entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Создание кнопки для входа в систему
button_login = tk.Button(root, text="Войти", command=log)
button_login.pack(pady=5)

# Создание метки для вывода результата
label_error = tk.Label(root, text="")
label_error.pack()

root.mainloop()