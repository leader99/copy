from tkinter.filedialog import *
import os
import glob
import time
import shutil
from tkinter import messagebox
from tkinter import ttk


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # путь
        self.txt = Text(self, width=30, height=1)
        self.txt.grid(row=0, column=1, columnspan=1, sticky=W)
        self.bttn1 = Button(self, text="Откуда", command=self.from_part, width=10, height=1)
        self.bttn1.grid(row=0, column=0, columnspan=1, sticky=W)
        self.txt1 = Text(self, width=30, height=1)
        self.txt1.grid(row=2, column=1, columnspan=1, sticky=W)
        self.bttn2 = Button(self, text="Куда", command=self.to_part, width=10, height=1)
        self.bttn2.grid(row=2, column=0, columnspan=1, sticky=W)
        # меню формата даты
        Label(self, text="Сортировать по:", width=20, height=1, bg="lightgray").grid(row=3, column=1)
        self.ear = BooleanVar()
        Checkbutton(self, text='Год', variable=self.ear, command=self.date_name).grid(row=4, column=0)
        self.mons = BooleanVar()
        Checkbutton(self, text='Месяц', variable=self.mons, command=self.date_name).grid(row=4, column=1)
        self.day = BooleanVar()
        Checkbutton(self, text='День', variable=self.day, command=self.date_name).grid(row=4, column=2)
        # меню типы файлов
        Label(self, text="Типы файлов", width=20, height=1, bg="lightgray").grid(row=5, column=1)
        self.var_tipe = IntVar()
        self.var_tipe.set(0)
        Radiobutton(self, text="Все файлы", variable=self.var_tipe, value=0).grid(row=6, column=0)
        Radiobutton(self, text="Выбор типа", variable=self.var_tipe, value=1).grid(row=6, column=1)
        # выбор формата
        self.f_ent = Entry(self, width=10)
        self.f_ent.grid(row=6, column=2, sticky=W)
        self.bttn4 = Button(self, text="Ok", command=self.f_name, width=3, height=1)
        self.bttn4.grid(row=6, column=3, columnspan=1, sticky=W)
        # копирование или перемещение
        Label(self, text="Способ сортировки", width=20, height=1, bg="lightgray").grid(row=7, column=1)
        self.var_copi = IntVar()
        self.var_copi.set(0)
        Radiobutton(self, text="Копирование", variable=self.var_copi, value=0).grid(row=8, column=0)
        Radiobutton(self, text="Перемещение", variable=self.var_copi, value=1).grid(row=8, column=1)
        # старт
        self.bttn3 = Button(self, text="Старт", command=self.copy, width=34, height=1)
        self.bttn3.grid(row=9, column=1, columnspan=1, sticky=W)
        # прогресбар
        self.progress = ttk.Progressbar(self, orient="horizontal", length=100, mode="determinate")
        self.progress.grid(row=10, column=1, pady=2, padx=2, sticky=E + W + N + S)
        self.progress["value"] = 0

    # тип файла
    def f_name(self):
        global file_extension
        file_extension = '*.' + self.f_ent.get()

    # название папки
    def date_name(self):
        global d_name
        d_name = ''
        if self.ear.get():
            d_name += '%Y'
        if self.mons.get():
            d_name += '-%m'
        if self.day.get():
            d_name += '-%d'

    # путь откуда копируем
    def from_part(self):
        global total_files
        global part_a
        part_a = askdirectory()
        # считаем фаилы
        total_files = 0
        for root, dirs, files in os.walk(part_a):
            for name in files:
                total_files += 1
        self.txt.delete(0.0, END)
        self.txt.insert(0.0, part_a)

    # путь куда копируем
    def to_part(self):
        global part_b
        part_b = askdirectory()
        self.txt1.delete(0.0, END)
        self.txt1.insert(0.0, part_b)

    # копирование
    def copy(self):
        # ловим ошибки заполнения
        try:
            a = part_a
        except NameError:
            messagebox.showerror("Error", "Не выбран путь откуда!")
        try:
            b = part_b
        except NameError:
            messagebox.showerror("Error", "Не выбран путь куда!")
        try:
            d = d_name
        except NameError:
            messagebox.showerror("Error", "Не выбран способ сортировки!")
        try:
            # считаем проценты прогресбара
            p = total_files
            percent = 100 / p
        except ZeroDivisionError:
            messagebox.showerror("Error", "В папке нет файлов!")

        var_tipe = self.var_tipe.get()
        var_copi = self.var_copi.get()

        # простое копирование
        if var_tipe is 0:
            for root, dirs, files in os.walk(a):
                for name in files:
                    a_name = os.path.join(root, name)
                    list_file = glob.glob(a_name)
                    for nameFile in list_file:
                        only_name = os.path.basename(nameFile)
                        time_str = time.strftime(d, time.gmtime(os.path.getmtime(nameFile)))
                        new_dir = os.path.join(b, time_str)
                        new_full_path = os.path.realpath(os.path.join(new_dir, only_name))
                        if not os.path.exists(new_dir):
                            os.makedirs(new_dir)
                        if var_copi is 0:
                            self.progress["value"] += percent
                            self.progress.update()
                            shutil.copy(nameFile, new_full_path)
                        else:
                            self.progress["value"] += percent
                            self.progress.update()
                            shutil.move(nameFile, new_full_path)
            messagebox.showinfo("Information", "Скопировано!")

        # копирование по типу файла
        else:
            try:
                f = file_extension
            except NameError:
                messagebox.showerror("Error", "Не выбран тип файла!")
            for root, dirs, files in os.walk(a):
                maska = os.path.join(root, f)
                list_file = glob.glob(maska)
                for nameFile in list_file:
                    only_name = os.path.basename(nameFile)
                    percent = 100 / len(list_file)
                    print(percent)
                    time_str = time.strftime(d, time.gmtime(os.path.getmtime(nameFile)))
                    new_dir = os.path.join(b, time_str)
                    new_full_path = os.path.realpath(os.path.join(new_dir, only_name))
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    if var_copi is 0:
                        self.progress["value"] += percent
                        self.progress.update()
                        shutil.copy(nameFile, new_full_path)
                    else:
                        self.progress["value"] += percent
                        self.progress.update()
                        shutil.move(nameFile, new_full_path)
            messagebox.showinfo("Information", "Скопировано!")
        self.progress["value"] = 0

root = Tk()
root.title("Copy")
root.geometry("445x250")
app = Application(root)
root.mainloop()
