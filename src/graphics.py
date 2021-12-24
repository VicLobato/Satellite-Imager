from tkinter import messagebox     # Error display
import tkinter as tk               # Tkinter

class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Satellite Imager')
        self.root.iconbitmap('logo.ico')
        self.can = tk.Canvas(self.root, width=600, height=600)
        self.can.pack(fill=tk.BOTH, expand=1)
        self.imgs = []

    def __repr__(self):
        return f'__SatelliteImager.Graphics'

    def addImg(self, x, y):
        self.img = tk.PhotoImage(file='temp.png')
        self.imgs.append(self.img)
        self.can.create_image(x, y, anchor=tk.NW, image=self.img)

    def error(self, message):
        messagebox.showerror('Fatal error', message)
        del self

    def clr(self):
        for w in self.root.winfo_children():
            w.destroy() 

    def upd(self):
        self.root.update()