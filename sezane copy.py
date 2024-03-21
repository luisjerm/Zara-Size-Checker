import sys
import time
import asyncio
from telegram import Bot
####
import requests
from bs4 import BeautifulSoup as bs
#import random
#import pandas as pd
#import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import random

from data import (TOKEN)
bot = Bot(token=TOKEN)
####

# realiza una espera aleatoria 
def timepoAleatorio(val):
    ranges = [i for i in range(3, val+1)]
    return random.choice(ranges)


# eleccion aletoria de user agent
def agenteUsuario():
    with open('user_agents.txt') as f:
        user_agents = f.read().split("\n")
        return random.choice(user_agents)   

async def operaciones_largas(parametros):
    try:
        # Dividir los parámetros en dos strings
        parametro1, parametro2= parametros.split()
        precioAnterior = 0
        while 1:
            # Se inicia la ventana del navegador con ventana en segundo plano
            chrome_options = webdriver.ChromeOptions()
            # user-agent aleatorio
            userAgent = agenteUsuario()
            print('User-agent:', userAgent)
            chrome_options.add_argument(f'user-agent={userAgent}')
            browser = uc.Chrome(options=chrome_options)
            #obtenemos url
            browser.get(parametro1)
            browser.implicitly_wait(10)
            # cookies continuar sin aceptar
            browser.find_element("xpath",'//*[@class="onetrust-close-btn-handler banner-close-button ot-close-link"]').click()
         
            browser.implicitly_wait(10)

            #bolsos
            browser.find_element("xpath",'/html/body/header/div/div/div/div/div/div[2]/div[3]/div/div[1]/nav/ul/li[3]/a').click()
            #refrescamos porque sale un mensaje de que hay que recargar
            browser.refresh()
            html = browser.page_source
            soup = bs(html, 'html.parser')

            browser.close()
            browser.quit()
          
            if 'precio' in parametro2:
                # Obtenemos el precio
                precio = soup.find('span', {'class': 'a-offscreen'}).text

                # Suprimimos el símbolo de la moneda
                precio = precio.replace('€', '')
                # Quitamos espacios
                precio = precio.strip()
                precio = precio.replace(',', '.')
                if precioAnterior == 0:
                    precioAnterior = precio
                # si ha bajado el precio notificamos
                if precio < precioAnterior:
                    resultado = f"El precio ha bajado! \r\n{parametro1}"
                    return resultado
                elif precio > precioAnterior:
                    resultado = f"El precio ha subido! \r\n{parametro1}"
            else:
                # Evaluamos la talla
                tallas = soup.find('div', {'class': 'Variant_product-variant-container__LkAwI'})
                print(tallas)
                # recorro buscado el texto de los label
                for i in tallas.find_all('label'):
                    item_talla = i.text.strip()
                    # print(item_talla)
                    # si el texto sin espacios es igual al parametro
                    if parametro2 in item_talla:
                        # si el label tiene la clase out-of-stock
                        if 'Agotado' in item_talla:
                            # si esta fuera de stock
                            # print('Talla no disponible')
                            # Se duerme al proceso x segundos   
                            #await asyncio.sleep(20) 
                            break       
                        else:
                            # si esta disponible
                            resultado = f"Aquí lo tienes! \r\n{parametro1}"
                            print('Talla disponible')
                            return resultado
                        break
            # Se duerme al proceso x segundos
            espera = timepoAleatorio(20)
            await asyncio.sleep(espera)
    except Exception as e:
        raise RuntimeError(f"Error en operaciones_largas: {str(e)}")

async def main():
    parametros = sys.argv[1]
    user_id = sys.argv[2]

    try:
        resultado = await operaciones_largas(parametros)
        await bot.send_message(chat_id=user_id, text=f"{resultado}")
    except Exception as e:
        await bot.send_message(chat_id=user_id, text=f"Hubo un error: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())