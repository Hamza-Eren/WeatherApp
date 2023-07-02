# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 13:52:56 2023

@author: HamzaEren
"""

from tkinter import Tk, Label, PhotoImage
from PIL import Image, ImageTk

def delete_window():
    app.destroy()

def animation(count=0):
    global showAnimation, app, gif_label, imageObjet, frames
    newImage = imageObjet[count]
    gif_label.configure(image=newImage)
    count+=1
    if count == frames:
        count = 0
    showAnimation = app.after(30, lambda: animation(count))
    app.after(3000, delete_window)

def splashscreen():
    global showAnimation, app, gif_label, imageObjet, frames, count
    app = Tk()
    width = 530
    height = 430
    x = (app.winfo_screenwidth()//2) - (width//2)
    y = (app.winfo_screenheight()//2) - (height//2)
    app.geometry("{}x{}+{}+{}".format(width, height, x, y))
    app.resizable(0,0)
    
    image = Image.open("images/background.png")
    img = ImageTk.PhotoImage(image)
    lbl = Label(app, image=img)
    lbl.image = img
    lbl.place(x=-2, y=-2)
    
    photo = Image.open("images/infinity.gif")
    frames = photo.n_frames
    imageObjet = [PhotoImage(file="images/infinity.gif", format=f"gif -index {i}") for i in range(frames)]
    count = 0
    showAnimation = None
    
    gif_label = Label(app, image="")
    gif_label.configure(bg="#6EC5D3")
    gif_label.place(x=162,y=269)
    animation()
    
    app.overrideredirect(True)
    app.attributes("-topmost", True)
    app.mainloop()