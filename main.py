# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 15:05:59 2023

@author: HamzaEren
"""

from tkinter import Tk, Entry, Button, PhotoImage, Label, END
import tkintermapview
from PIL import ImageTk,Image
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import json
from splashscreen import splashscreen

url = "http://api.openweathermap.org/data/2.5/weather"
api_key = "cc811f7c871c4039a49a0074dd54522c"
iconUrl = "http://openweathermap.org/img/wn/{}@2x.png"
             
def getWeather(sehir):
    global sehirGirme
    params = {'q':sehir.upper().capitalize(), 'appid':api_key, 'lang':'tr'}
    data = requests.get(url,params=params).json()
    if data and data['cod'] == 200:
        icon = data['weather'][0]['icon']
        durum = data['weather'][0]['description'].capitalize()
        sicaklik = int(data['main']['temp'] - 273)
        sehir = data['name'].capitalize()
        ulke = data['sys']['country']
        ruzgar = data['wind']['speed']
        nem = data['main']['humidity']
        basinc = data['main']['pressure']
        bulut = data['clouds']['all']
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        x_coo = data['coord']['lat']
        y_coo = data['coord']['lon']
        if len(durum) > 24:
            durum = durum[:22] + '...'
        return (icon, durum, sicaklik, sehir, ulke, ruzgar, nem, basinc, bulut, sunrise, sunset, x_coo, y_coo)
    else:
        sehirGirme.delete(0, END)
        sehirGirme.insert(0, "Şehir bulunamadı !")
    
def main(*args):
    global sehirGirme, iconLabel, conditionLabel, tempLabel, locationLabel, windLabel, humLabel, preLabel, cloLabel, riseLabel, setLabel, maps
    sehir = sehirGirme.get()
    if sehir:
        weather = getWeather(sehir)
    if weather:
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconUrl.format(weather[0]),stream=True).raw))
        iconLabel.configure(image = icon)
        iconLabel.image = icon
        conditionLabel['text'] = "{}".format(weather[1])
        tempLabel['text'] = "{}°C".format(weather[2])
        locationLabel['text'] = "{}, {}".format(weather[3],weather[4])
        windLabel['text'] = "Rüzgar hızı: {}m/s".format(weather[5])
        humLabel['text'] = "Nem Oranı: {}%".format(weather[6])
        preLabel['text'] = "Basınç: {}mb".format(weather[7])
        cloLabel['text'] = "Bulutluluk: {}%".format(weather[8])
        riseLabel['text'] = "Gün doğumu: {}".format(dt.fromtimestamp(weather[9]).strftime("%H:%M"))
        setLabel['text'] = "Gün batımı: {}".format(dt.fromtimestamp(weather[10]).strftime("%H:%M"))
        maps.set_position(weather[11], weather[12])
        maps.place(x=225, y=225, width=250, height=175)

def mainApp():
    global sehirGirme, iconLabel, conditionLabel, tempLabel, locationLabel, windLabel, humLabel, preLabel, cloLabel, riseLabel, setLabel, maps
    splashscreen()
    app = Tk()
    app.iconbitmap('images/icon.ico')
    app.title('Hava Durumu')
    width = 530
    height = 430
    x = (app.winfo_screenwidth()//2) - (width//2)
    y = (app.winfo_screenheight()//2) - (height//2)
    app.geometry("{}x{}+{}+{}".format(width, height, x, y))
    app.resizable(0,0)
    
    sehirGirme = Entry(app)
    sehirGirme.bind('<Return>', main)
    sehirGirme.place(x=150, y=25, width=205, height=25)
    sehirGirme.focus()
    
    p1 = PhotoImage(file = "images/buyutec.png")
    search_btn = Button(app, image=p1, borderwidth=0, command=main)
    search_btn.place(x=355, y=22, width=26, height=26)
    
    iconLabel = Label(app)
    iconLabel.place(x=63, y=100, width=100, height=100)
    
    conditionLabel = Label(app, font=('Arial',12))
    conditionLabel.place(x=50, y=225, width=125, height=50)
    
    tempLabel = Label(app, font=('Arial',30,'bold'))
    tempLabel.place(x=50, y=300, width=125, height=50)
    
    locationLabel = Label(app, font=('Arial',15))
    locationLabel.place(x=50, y=375, width=125, height=25)
    
    windLabel = Label(app)
    windLabel.place(x=225, y=100, width=125, height=33)
    humLabel = Label(app)
    humLabel.place(x=350, y=100, width=125, height=33)
    preLabel = Label(app)
    preLabel.place(x=225, y=133, width=125, height=33)
    cloLabel = Label(app)
    cloLabel.place(x=350, y=133, width=125, height=33)
    riseLabel = Label(app)
    riseLabel.place(x=225, y=166, width=125, height=33)
    setLabel = Label(app)
    setLabel.place(x=350, y=166, width=125, height=33)
    
    maps = tkintermapview.TkinterMapView(app, width=800, height=600)
    maps.set_zoom(8)
    
    app.mainloop()
    
    
mainApp()