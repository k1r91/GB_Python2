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
        self.coords = self.screen_width // 2 - self.width // 2, \
                 self.screen_height // 2 - self.height // 2
        self.main_window.geometry('{}x{}+{}+{}'.
                        format(self.width, self.height,
                               self.coords[0], self.coords[1]))

        #create menu
        self.initialize_menu()
        # create StatusBar and other widgets
        self.initialize_widgets()
        self.controller = Controller()

    def default_callback(self):
        print("not implemented yet")

    def initialize_menu(self):
        main_menu = tk.Menu(self.main_window)

        # add database menu
        file_menu = tk.Menu(main_menu)

        file_menu.add_command(label='Terminals',
                              command=self.open_terminal_view)
        file_menu.add_command(label='Partners',
                              command=self.open_partner_view)
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

    def open_terminal_view(self):
        offset = 50
        t_window = View('terminal', h=300, w=900,
                        x=self.coords[0] + offset, y=self.coords[1] + offset)
        t_window.title('Terminals')
        t_window.transient(self.main_window)
        t_window.grab_set()
        self.main_window.wait_window(t_window)

    def open_partner_view(self):
        offset = 50
        t_window = View('partner', h=300, w=600,
                        x=self.coords[0] + offset, y=self.coords[1] + offset)
        t_window.title('Partners')
        t_window.transient(self.main_window)
        t_window.grab_set()
        self.main_window.wait_window(t_window)

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
