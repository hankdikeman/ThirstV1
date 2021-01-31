import tkinter as tk


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#E1C699',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()
        # self.canvas.create_rectangle(
        #    250, 300, 330, 320, fill='blue', tags='paddle')
