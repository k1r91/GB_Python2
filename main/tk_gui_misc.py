import getpass
import tkinter as tk
import os

from datetime import datetime

from DB import Sqlite3Db as DB


class StatusBar(tk.Frame):

    def __init__(self, parent=None, *args):
        super().__init__(parent)
        self.username = getpass.getuser()
        self.db_name = DB.DB_NAME
        self.pack(side=tk.BOTTOM)
        self.clock = tk.Label(self, text='time: {}'
                              .format(datetime.today().strftime('%H:%M:%S')))
        self.clock.pack(side=tk.RIGHT)
        self.clock.after(1000, self.tik_tak)
        self.information_label = tk.Label(self,
                                          text='database: {} / user: {} /'
                                          .format(self.db_name, self.username))
        self.information_label.pack(side=tk.LEFT)
        self.pack()

    def tik_tak(self):
        self.clock.config(text='time: {}'
                          .format(datetime.today().strftime('%H:%M:%S')))
        self.clock.after(1000, self.tik_tak)


class TableGrid(tk.Frame):

    def __init__(self, parent=None, titles=None, rows=0, *args, **kwargs):
        width = kwargs.get('w', 300)
        height = kwargs.get('h', 300)
        super().__init__(parent, relief=tk.GROOVE, width=width,height=height,
                         bd=1)
        self.width = width
        self.height= height
        self._create_scroll()
        for index, title in enumerate(titles):
            tk.Label(self.frame, text=title).grid(row=0, column=index)

        self.rebuild(len(titles), rows)
        self.pack()

    def _create_scroll(self):
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                      command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left')
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        self.frame.bind('<Configure>', lambda e: self._scroll())

    def _scroll(self):
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        self.canvas.config(width=self.width, height=self.height)

    def rebuild(self, rows=0, columns=0):
        self.vars = []
        self.cells = []
        for i in range(1, rows+1):
            self.vars.append([])
            for j in range(columns):
                var = tk.StringVar()
                self.vars[i-1].append(var)
                cell = tk.Entry(self.frame, textvariable=var)
                cell.grid(row=i, column=j)
                self.cells.append(cell)
            '''if columns != 0:
                img_path = os.path.join('img', 'insert.gif')
                img = tk.PhotoImage(file=img_path)
                cell = tk.Button(image=img,
                                command=self.default_callback)
                cell.grid(row=i, column=columns+1)
                self.cells.append(cell)'''


    def update_data(self, data_func):
        sql_data = data_func()
        self.rebuild(len(sql_data), len(sql_data[0]))
        for index, data in enumerate(sql_data):
            for i, d in enumerate(data):
                self.vars[index][i].set(d)

    def default_callback(self):
        print("not implemented yet")