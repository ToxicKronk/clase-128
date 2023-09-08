from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# Enlace a NASA Exoplanet
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Controlador web
browser = webdriver.Chrome("C:/Users/Owen/Downloads/PRO_C128_AA1_V1-main/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    
    ## AGREGA CÓDIGO AQUÍ ##

    try: 
        result_page = requests.get( hyperlink)
        soup=BeautifulSoup(browser.page_source, "html.parser")
        temp_data = []
        for row in soup.find_all("tr", attrs= {"class": "fact_row"}):
            td_tag = row.find_all("td")
            for recorrido in td_tag:
                try:
                    temp_data.append(recorrido.find_all("div", attrs= {"class": "value"})[0].contents[0])
                except:
                    temp_data.append("")
        new_planets_data.append(temp_data)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)





planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Llamar al método
for index, row in planet_df_1.iterrows():

     ## ADGREGA CÓDIGO AQUÍ ##
    print(row["hyperlink"])
     # Llama a scrape_more_data(<hyperlink>)
    scrape_more_data(row["hyperlink"])
    print(f"La extracción de datos del hipervínculo {index+1} se ha completado")

print(new_planets_data[0:10])

# Remover el carácter '\n' de los datos extraídos
scraped_data = []

for row in new_planets_data:
    replaced = []
    ## AGREGAR EL CÓDIGO AQUÍ ##
    for columns in row:
        columns = columns.replace("\n", " ")
        replaced.append(columns)    
    scraped_data.append(replaced)

print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convertir a CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
