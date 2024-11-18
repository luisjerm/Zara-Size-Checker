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

from data import (TOKEN)
bot = Bot(token=TOKEN)
####
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())

####


async def operaciones_largas(strParametros):
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
        chrome_options = webdriver.ChromeOptions()
        userAgent = agenteUsuario()
        chrome_options.add_argument(f'user-agent={userAgent}')
        browser = uc.Chrome(options=chrome_options)
        browser.get(url)
        # cookies, subimos tiempo, antes 5s saltaba error porque tenian cuenta atras
        WebDriverWait(browser, 30)\
            .until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-reject-all-handler"]')))\
            .click()
        #browser.find_element("xpath",'//*[@id="onetrust-reject-all-handler"]').click()
        found = True
        if(talla != ''):
            # desplegamos tamanos
            WebDriverWait(browser, 5)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dropdown-input')))\
                .click()
            # browser.find_element(By.CSS_SELECTOR, 'div.dropdown-input').click()

            # evaluamos si existe el tamaño indicado
            # en div.container-size vertical se almacena la lista de tamaños
            #sizes = browser.find_element(By.CSS_SELECTOR, 'div.container-size.vertical')
            # recorremos los div.size-element__container de sizes para buscar el tamaño
            found = False
            #for i in sizes.find_elements(By.CSS_SELECTOR, 'div.size-element__container'):
            for i in browser.find_elements(By.CSS_SELECTOR, 'div.size-element__container'):
                size = i.find_element(By.CSS_SELECTOR, 'span.size-label').text
                if talla in size:
                    found = True
                    i.click()
                    '''if not precio:
                        resultado = f"Aquí lo tienes! \r\n {url}"
                        return resultado
                    break'''
        if found:
            #print('Talla disponible')
            # evaluamos el precio
            precioValor = browser.find_element(By.CSS_SELECTOR, 'span.price-unit--normal.product-detail-price').text
        #else:
            #print('Talla no disponible')

        #browser.close()
        browser.quit()
        
        if checkPrize == True:
            # Suprimimos el símbolo de la moneda
            precioValor = precioValor.replace('€', '')
            # Quitamos espacios
            precioValor = precioValor.strip()
            precioValor = float(precioValor.replace(',', '.'))
            if precio == -1:
                precio = precioValor
            if initialPrize == -1:
                initialPrize = precioValor
            notif = check(talla, found, precioValor, initialPrize, variacion, targetPrize)
            parametros = updateEntry(parametros, precio, initialPrize, notif)
            return parametros
        
    except Exception as e:
        raise RuntimeError(f"Error en operaciones_largas {frameinfo.filename}: {str(e)}")

async def main():
    parametros = sys.argv[1]

    try:
        resultado = await operaciones_largas(parametros)
        user = resultado['user']
         # Si el producto esta disponible o ha bajado de precio se envia un mensaje
        '''if resultado['notify'] == True:
            await bot.send_message(chat_id=user, text=f"Aquí tienes lo que estabas esperando")'''
        print(resultado)
    except Exception as e:
        # await bot.send_message(chat_id=user, text=f"Hubo un error: {str(e)}")
        print(f"Hubo un error {str(frameinfo)}: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())