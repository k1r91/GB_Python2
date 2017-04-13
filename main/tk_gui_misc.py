import getpass
import tkinter as tk
import os

from PIL import Image

from datetime import datetime

from DB import Sqlite3Db as DB

from controller import Controller


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


class View(tk.Toplevel):

    def __init__(self, table, h, w, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cells = []
        self.table = table
        self.controller = Controller()
        self.geometry("%dx%d%+d%+d" % (w, h, x, y))
        self.w = w
        self.h = h
        self.data = self.controller.get_table_info(self.table)
        self.columns = len(self.data[0])
        self._create_scroll()
        # columns - number of titles +2 buttons
        self.rebuild()

    def _place_titles(self, titles):
        for index, title in enumerate(titles):
            tk.Label(self.frame, text=title).grid(row=0, column=index)

    def configure_grid(self):
        for column in range(self.columns):
            self.frame.columnconfigure(column, weight=1)

    def rebuild(self):
        self.refresh_data()
        for widget in self.frame.grid_slaves():
            widget.grid_forget()
        self.configure_grid()
        self._place_titles(self.data[0])
        self.cells = []
        self.widgets = []
        values = self.data[1:]
        for i in range(len(values)):
            self.cells.append(values[i])
            self.widgets.append([])
            for index, value in enumerate(values[i]):
                cell_text = tk.StringVar()
                cell_text.set(value)
                cell = tk.Entry(self.frame, textvariable=cell_text,
                                state='readonly')
                cell.grid(row=i+1, column=index)
                self.widgets[i].append(cell)

            self.place_buttons(i)

    def place_buttons(self, i):
        btn_edit = EditButton(self.frame)
        btn_edit.set_environment(self, i)
        btn_edit.grid(row=i + 1, column=self.columns)

        btn_delete = DeleteButton(self.frame)
        btn_delete.set_environment(self, i)
        btn_delete.grid(row=i + 1, column=self.columns + 2)

    def refresh_data(self):
        self.data = self.controller.get_table_info(self.table)

    def _create_scroll(self):
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                      command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(fill=tk.BOTH)
        self.canvas_frame = self.canvas.create_window((0,0),
                                                      window=self.frame,
                                                      anchor='nw')
        self.frame.bind("<Configure>", lambda e: self._scroll())
        self.canvas.bind('<Configure>', self.frame_width)

    def frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def _scroll(self):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=self.w, height=self.h)


class TableButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.height = 20
        self.width = 20
        self.set_image()
        self.config(command=self.exec)
        self.table = None
        self._id = None
        self.controller = None

    def set_environment(self, frame, _id):
        self.frame = frame
        self.table = frame.table
        self._id = _id
        self.controller = frame.controller

    def set_image(self):
        pass

    def set_exec(self):
        pass


class EditButton(TableButton):
    def __init__(self, *args, **kwargs):
        self.img = None
        self.state = 'edit'
        self.old_state = None
        super().__init__(*args, **kwargs)

    def set_image(self):
        if self.state is 'edit':
            self.config_image('rsz_edit.gif')
        else:
            self.config_image('rsz_accept.gif')

    def config_image(self, img_file):
        img_file = os.path.join('img', img_file)
        image = tk.PhotoImage(file=img_file)
        self.config(image=image, height=self.height, width=self.width)
        self.img = image

    def switch_state(self):
        if self.state is 'edit':
            self.state = 'accept'
        else:
            self.state = 'edit'

    def exec(self):
        if self.state is 'edit':
            self.old_state = [x.get() for x in self.frame.widgets[self._id]]
            for entry in self.frame.widgets[self._id]:
                entry.config(state='normal')
        else:
            data = [x.get() for x in self.frame.widgets[self._id]]
            if set(self.old_state) != set(data):
                self.write_changes(data, self.old_state[0])
            for entry in self.frame.widgets[self._id]:
                entry.config(state='readonly')
        self.switch_state()
        self.set_image()

    def write_changes(self, data, id):
        self.controller.update(self.table, data, id)


class DeleteButton(TableButton):

    def __init__(self, *args, **kwargs):
        self.img = None
        super().__init__(*args, *kwargs)

    def set_image(self):
        img_file = os.path.join('img', 'rsz_delete.gif')
        image = tk.PhotoImage(file = img_file)
        self.config(image=image, height=self.height, width=self.width)
        self.img = image

    def exec(self):
        id_to_delete = self.frame.cells[self._id][0]
        self.controller.delete_from(self.table, id_to_delete)
        self.frame.rebuild()
