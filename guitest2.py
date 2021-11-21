import tkinter as tk
from tkinter import filedialog
import glob
import os

root = tk.Tk()
root.title('Julius-Freezer GUI')
root.geometry('600x400')

def showing(e):
    n = lst.curselection()
    frame = lst.get(n)
    img = tk.PhotoImage(file=fname)
    lab.config(image=img)
    lab.image = img
    print(fname)

lst = tk.Listbox(root)
lst.pack(side="left", fill=tk.Y, expand=1)
namelist = [i for i in glob.glob("*jpg")]
for frame in namelist:
    lst.insert(tk.END, fname)
lst.bind("<<ListboxSelect>>", showing)
img = tk.Photoimage(file="Idle (5)_ltl.jpg")
lab = tk.Label(root, text="hello", image=img)
lab.pack(side="left")

root.mainloop()


