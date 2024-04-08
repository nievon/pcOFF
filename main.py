import tkinter as tk
from tkinter import PhotoImage
import subprocess

# IP-адреса компьютеров
computers = [
    "10.134.14.53",
    "10.134.14.54",
    "10.134.14.55",
    "10.134.14.56",
    "10.134.14.61",
    "10.134.14.58",
    "10.134.14.60",
    "10.134.14.201",
    "10.134.14.63",
    "10.134.14.203"
]

# Функция для вызова команды shutdown для конкретного IP-адреса
def shutdown_windows(ip, message, time, option):
    try:
        if option == "shutdown":
            subprocess.run(["shutdown", "/m", ip, "/s", "/f", "/c", message, "/t", str(time)], check=True)
        elif option == "restart":
            subprocess.run(["shutdown", "/m", ip, "/r", "/f", "/c", message, "/t", str(time)], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


# Функция для отмены выключения на конкретном компьютере
def cancel_shutdown_computer(ip):
    subprocess.run(["shutdown", "/m", ip, "/a"])


# Функция для выключения всех компьютеров
def shutdown_all_computers():
    selected_computers.clear()
    message = message_entry.get()
    time = int(time_entry.get())
    option = selected_option.get()
    for i, ip in enumerate(computers, start=1):
        success = shutdown_windows(ip, message, time, option)
        if success:
            buttons[i - 1].config(bg="green")
            selected_computers.append(ip)
        else:
            buttons[i - 1].config(bg="red")


# Создаем главное окно
root = tk.Tk()
root.title("pcOFF")

# Заголовок окна
title_label = tk.Label(root, text="Admin Panel", font=("Helvetica", 20, "italic", "bold"))
title_label.pack(pady=10)
root.iconbitmap('ico.ico')

# Загружаем изображение иконки ПК
pc_icon = PhotoImage(file="pc.png")

# Фрейм для кнопок
button_frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
button_frame.pack(pady=10)

# Создаем кнопки для каждого компьютера с нумерацией и иконкой ПК
buttons = []
cancel_buttons = []
for i, ip in enumerate(computers, start=1):
    button_frame_inner = tk.Frame(button_frame, bg="white")
    button_frame_inner.grid(row=(i - 1) // 4, column=(i - 1) % 4, sticky="ew")

    button = tk.Button(button_frame_inner, text=f"{i}. {ip}", image=pc_icon, compound=tk.LEFT,
                       command=lambda ip=ip: shutdown_windows(ip, message_entry.get(), int(time_entry.get()),
                                                              selected_option.get()), bd=0, bg="white",
                       relief=tk.GROOVE, padx=10, pady=5, borderwidth=5)
    button.pack(side=tk.LEFT)
    buttons.append(button)

    cancel_button = tk.Button(button_frame_inner, text="❌", command=lambda ip=ip: cancel_shutdown_computer(ip), bd=0,
                              bg="white", relief=tk.GROOVE, padx=5, pady=2, borderwidth=3)
    cancel_button.pack(side=tk.LEFT, padx=5)
    cancel_buttons.append(cancel_button)

# Поле ввода для текста уведомления
message_label = tk.Label(root, text="Текст уведомления:")
message_label.pack()
message_entry = tk.Entry(root)
message_entry.pack()

# Поле ввода времени до выключения
time_label = tk.Label(root, text="Время до выключения (в секундах):")
time_label.pack()
time_entry = tk.Entry(root)
time_entry.pack()

# Опции перезагрузки или завершения
selected_option = tk.StringVar(value="shutdown")
shutdown_radio = tk.Radiobutton(root, text="Завершение", variable=selected_option, value="shutdown")
shutdown_radio.pack()
restart_radio = tk.Radiobutton(root, text="Перезагрузка", variable=selected_option, value="restart")
restart_radio.pack()

# Кнопка для выключения всех компьютеров
shutdown_all_button = tk.Button(root, text="Выключить все компьютеры", command=shutdown_all_computers)
shutdown_all_button.pack(pady=10)

# Список выбранных компьютеров для выключения
selected_computers = []

# Запускаем главный цикл обработки событий
root.mainloop()

