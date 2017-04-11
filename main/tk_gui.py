import tkinter as tk

from tk_gui_misc import *
from controller import Controller

class MainGui:

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('Manage transaction server')
        self.screen_height = self.main_window.winfo_screenheight()
        self.screen_width = self.main_window.winfo_screenwidth()
        self.height = 400
        self.width = 850
        self.terminal_grid = None
        coords = self.screen_width // 2 - self.width // 2, \
                 self.screen_height // 2 - self.height // 2
        self.main_window.geometry('{}x{}+{}+{}'.
                        format(self.width, self.height, coords[0], coords[1]))

        #create menu
        self.initialize_menu()
        # create StatusBar and other widgets
        self.initialize_widgets()
        self.controller = Controller()

    def default_callback(self):
        print("not implemented yet")

    def sql_get_terminals(self):
        ''' SQL-заглушка
        '''
        ls = []
        for i in range(40):
            ls.append((i, 'Терминал_{}'.format(i), 'описание...'))
        return ls

    def initialize_menu(self):
        main_menu = tk.Menu(self.main_window)

        # add database menu
        file_menu = tk.Menu(main_menu)

        file_menu.add_command(label='Terminals',
                              command=self.pack_terminal_grid)
        file_menu.add_command(label='Partners', command=self.default_callback)
        file_menu.add_command(label='Transactions',
                              command=self.default_callback)
        main_menu.add_cascade(label='Database', menu=file_menu)

        # add help menu
        help_menu = tk.Menu(main_menu)
        help_menu.add_command(label='Help', command=self.default_callback)
        help_menu.add_command(label='About the program',
                              command=self.default_callback)
        main_menu.add_cascade(label='Help', menu=help_menu)

        # place main menu
        self.main_window.config(menu=main_menu)

    def initialize_widgets(self):
        statusbar = StatusBar(self.main_window)

    def pack_terminal_grid(self):
        if self.terminal_grid is not None:
            self.terminal_grid.pack_forget()
        self.terminal_grid = TableGrid(None, ('Terminal id',
                                              'Configuration file',
                                              'Title',
                                              'Description',
                                              'Public key'),
                         0, w=self.width)
        self.terminal_grid.update_data(self.controller.get_terminals)

    def place_buttons(self):
        img_path = os.path.join('img', 'insert.gif')
        img = tk.PhotoImage(file=img_path)
        btn = tk.Button(self.main_window, image=img,
                        command=self.default_callback)
        btn.pack(side=tk.LEFT)
        btn.img = img

    def mainloop(self):
        self.main_window.mainloop()


def main():
    gui = MainGui()
    gui.mainloop()

if __name__ == '__main__':
    main()
