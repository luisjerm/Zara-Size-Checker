import sys
import time
import asyncio
from telegram import Bot
####
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
# esperas para que aparezcan elementos en la web
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import json
from utils import *
from WebScrapper.WebScrapper import WebScrapper

from data import (TOKEN)
bot = Bot(token=TOKEN)
####
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())
####

async def operaciones_largas(parametros):
    try:
        # Genero un diccionario con los parametros
        parametros = json.loads(strParametros)
        url = parametros['url']
        precioInfo = parametros['prizeInfo']
        precio = precioInfo['prize']
        initialPrize = precioInfo['initialPrize']
        variacion = precioInfo['variation']
        targetPrize = precioInfo['targetPrize']
        checkPrize = precioInfo['checkPrize']
        talla = parametros['size']
        
        # Se inicia la ventana del navegador con ventana en segundo plano
        browser = WebScrapper()
        res = browser.getPage(url)
        # Aceptamos cooquiesz
        # cookies, subimos tiempo, antes 5s saltaba error porque tenian cuenta atras
        res = browser.clickElemByXpath('//*[@id="onetrust-accept-btn-handler"]', timeout=30)
        found = True


        if(talla != ''):
            tallas = browser.getElement('div.size-element__container')
        if precio:
            # Obtenemos el precio
            precioValor = soup.find('div', {'class': 'Product_product-price__FHmFJ'}).text
            # Suprimimos el símbolo de la moneda
            precioValor = precioValor.replace('€', '')
            # Quitamos espacios
            precioValor = precioValor.strip()
            precioValor = precioValor.replace(',', '.')
            if precioAnterior == 0:
                precioAnterior = precioValor
            # si ha bajado el precio notificamos
            if precioValor < precioAnterior:
                resultado = f"El precio ha bajado! \r\n{url}"
            else:
                resultado = str(precioValor)
            return resultado
        else:
            # Evaluamos la talla
            tallas = soup.find('div', {'class': 'Variant_product-variant-container__LkAwI'})
            #print(tallas)
            # recorro buscado el texto de los label
            for i in tallas.find_all('label'):
                item_talla = i.text.strip()
                # print(item_talla)
                # si el texto sin espacios es igual al parametro
                if talla in item_talla:
                    # si el label tiene la clase out-of-stock
                    if 'Agotado' in item_talla:
                        # si esta fuera de stock
                        # print('Talla no disponible')
                        # Se duerme al proceso x segundos   
                        #await asyncio.sleep(20) 
                        resultado = f"La talla no está disponible \r\n{url}"
                        break       
                    else:
                        # si esta disponible
                        resultado = f"Aquí lo tienes! \r\n{url}"
                        #print('Talla disponible')
                    break
            return resultado
    except Exception as e:
        raise RuntimeError(f"Error en operaciones_largas: {str(e)}")

async def main():
    parametros = sys.argv[1]

    try:
        resultado = await operaciones_largas(parametros)
        print(resultado)
    except Exception as e:
        print(f"Hubo un error {str(frameinfo)}: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())