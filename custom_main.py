# -*- coding: utf-8 -*-
"""
@author: HamzaEren
"""

from tkinter import Tk, Entry, Button, PhotoImage, Label, END, W
from customtkinter import CTk, CTkEntry, CTkImage, CTkButton, CTkLabel
import customtkinter
customtkinter.set_appearance_mode("dark")
import tkintermapview
from PIL import ImageTk,Image
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import json
from splashscreen import splashscreen

url = "http://api.openweathermap.org/data/2.5/weather"
api_key = "YOUR API_KEY"
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
        conditionLabel.configure(text= "{}".format(weather[1]))
        tempLabel.configure(text = "{}°C".format(weather[2]))
        locationLabel.configure(text = "{}, {}".format(weather[3],weather[4]))
        windLabel.configure(text = "Rüzgar hızı: {}m/s".format(weather[5]))
        humLabel.configure(text = "Nem Oranı: {}%".format(weather[6]))
        preLabel.configure(text = "Basınç: {}mb".format(weather[7]))
        cloLabel.configure(text = "Bulutluluk: {}%".format(weather[8]))
        riseLabel.configure(text = "Gün doğumu: {}".format(dt.fromtimestamp(weather[9]).strftime("%H:%M")))
        setLabel.configure(text = "Gün batımı: {}".format(dt.fromtimestamp(weather[10]).strftime("%H:%M")))
        maps.set_position(weather[11], weather[12])
        maps.place(x=275, y=275, width=275, height=200)

def mainApp():
    global sehirGirme, iconLabel, conditionLabel, tempLabel, locationLabel, windLabel, humLabel, preLabel, cloLabel, riseLabel, setLabel, maps
    splashscreen()
    app = CTk()
    app.iconbitmap('images/icon.ico')
    app.title('Hava Durumu')
    width = 530
    height = 430
    x = (app.winfo_screenwidth()//2) - (width//2)
    y = (app.winfo_screenheight()//2) - (height//2)
    app.geometry("{}x{}+{}+{}".format(width, height, x, y))
    app.resizable(0,0)
        
    sehirGirme = CTkEntry(app, placeholder_text="Şehir girin..", corner_radius=10, width=205, height=25)
    sehirGirme.bind('<Return>', main)
    sehirGirme.place(x=150, y=25)
    #sehirGirme.focus()
        
    p1 = CTkImage(Image.open("images/buyutec.png"))
    search_btn = CTkButton(app, image=p1, text="Ara", width=26, height=26, command=main)
    search_btn.place(x=355, y=22)
      
    iconLabel = CTkLabel(app, text="", width=100, height=100)
    iconLabel.place(x=63, y=100)
       
    conditionLabel = CTkLabel(app, text="", font=('Arial',12), width=125, height=50)
    conditionLabel.place(x=50, y=225)
       
    tempLabel = CTkLabel(app, text="", font=('Arial',30,'bold'), width=125, height=50)
    tempLabel.place(x=50, y=300)
       
    locationLabel = CTkLabel(app, text="", font=('Arial',15), width=125, height=25)
    locationLabel.place(x=50, y=375)
        
    windLabel = CTkLabel(app, text="", anchor=W, width=125, height=33)
    windLabel.place(x=220, y=100)
    humLabel = CTkLabel(app, text="", anchor=W, width=125, height=33)
    humLabel.place(x=350, y=100)
    preLabel = CTkLabel(app, text="", anchor=W, width=125, height=33)
    preLabel.place(x=220, y=133)
    cloLabel = CTkLabel(app, text="", anchor=W, width=125, height=33)
    cloLabel.place(x=350, y=133)
    riseLabel = CTkLabel(app, text="", anchor=W, width=125, height=33)
    riseLabel.place(x=220, y=166)
    setLabel = CTkLabel(app, text="", anchor=W, width=125, height=33)
    setLabel.place(x=350, y=166)
       
    maps = tkintermapview.TkinterMapView(app, width=800, height=600)
    maps.set_zoom(8)
        
    app.mainloop()
    
mainApp()
