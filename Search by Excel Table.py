# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 16:11:40 2020

@author: e.rios.kaliman
"""

import time
from os import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from pandas import read_excel


peliculas=[]
generos_disponibles=["Biography","Drama","Animation","Adventure","Comedy","Family","Terror","Action","No encontrado"]

data = pd.read_excel(r'C:\Users\e.rios.kaliman\Desktop\Lista_peliculas.xlsx')

for index,row in data.iterrows():
    peliculas.append(row["Peliculas"])
    
print(peliculas)
print("BUSCADOR DE PELICULAS :)")
cantidad_peliculas = int(input("Cuantas peliculas desea buscar?: "))

for i in range (cantidad_peliculas):
    peli = input("Nombre de pelicula: ")
    peliculas.append(peli)

user = environ["USERPROFILE"]
ch_options = webdriver.ChromeOptions()
ch_options.add_argument("user-data-dir=" + user +
                     "\\AppData\\Local\\Google\\Chrome\\User Data")

driver = webdriver.Chrome(executable_path=r'C:\Users\e.rios.kaliman\Desktop\chromedriver.exe',
                          options=ch_options)

driver.get("https://www.imdb.com/")
rating=[]
duracion=[]
sinopsis=[]
genero=[]

for peli in peliculas:
    
    time.sleep(5)
    
    search=driver.find_element_by_xpath('//*[@id="suggestion-search"]')
       
    search.send_keys(peli)
    search.send_keys(Keys.ENTER)
    
    time.sleep(5)
    
    peliculas_click = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[1]/td[2]/a')
    peliculas_click.click()
    
    try:    
        rating_peli = driver.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span').text
        rating.append(rating_peli)
        
        duracion_peli = driver.find_element_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/time').text
        duracion.append(duracion_peli)
        
        sinopsis_peli = driver.find_element_by_xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[1]').text
        sinopsis.append(sinopsis_peli)
        
        genero_peli = driver.find_elements_by_xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/a')
        genero.append([genero.text for genero in genero_peli])
        genero.pop()
    
    except NoSuchElementException:    
        rating.append("No encontrado")
        duracion.append("No encontrado")
        sinopsis.append("No encontrado")
        genero.append("No encontrado")
    
    driver.get("https://www.imdb.com/")


for i in genero:
    if type(i) ==list:
        i.pop()
    

Diccionario =  {"Pelicula":peliculas,"Duracion":duracion,"Genero":genero,"Sinopsis":sinopsis,"Rating":rating}

df_peliculas = pd.DataFrame(Diccionario)

df_peliculas.to_excel(r'C:\Users\e.rios.kaliman\Desktop\PYTHON\Peliculas.xls',sheet_name="Peliculas IMDB",index=False)

driver.quit()
