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
import random

from data import (TOKEN)
bot = Bot(token=TOKEN)
####
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())

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
        #parametro1, parametro2, parametro3= parametros.split()
        paramList = parametros.split()
        url = ''
        precio = False
        talla = ''
        precioAnterior = 0
        for i in range(0, len(paramList)):
            if i == 0:
                url = paramList[i]
                continue
            if 'precio' in paramList[i]:
                precio = True
                precioAnterior = float(paramList[i].split('=')[1])
            else: 
                talla = paramList[i]

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
            sizes = browser.find_element(By.CSS_SELECTOR, 'div.container-size.vertical')
            # recorremos los div.size-element__container de sizes para buscar el tamaño
            found = False
            for i in sizes.find_elements(By.CSS_SELECTOR, 'div.size-element__container'):
                size = i.find_element(By.CSS_SELECTOR, 'span.size-label').text
                if talla in size:
                    found = True
                    i.click()
                    if not precio:
                        resultado = f"Aquí lo tienes! \r\n {url}"
                        return resultado
                    break
        if found:
            #print('Talla disponible')
            # evaluamos el precio
            precioValor = browser.find_element(By.CSS_SELECTOR, 'span.price-unit--normal.product-detail-price').text
        #else:
            #print('Talla no disponible')

        #browser.close()
        browser.quit()
        
        if precio :
            # Suprimimos el símbolo de la moneda
            precioValor = precioValor.replace('€', '')
            # Quitamos espacios
            precioValor = precioValor.strip()
            precioValor = float(precioValor.replace(',', '.'))
            if precioAnterior == 0:
                precioAnterior = precioValor
            # si ha bajado el precio notificamos
            if precioValor < precioAnterior:
                resultado = f"El precio ha bajado! \r\n{url}"
            else:
                resultado = str(precioValor)
            return resultado
    except Exception as e:
        raise RuntimeError(f"Error en operaciones_largas {frameinfo.filename}: {str(e)}")

async def main():
    parametros = sys.argv[1]
    user_id = sys.argv[2]

    try:
        resultado = await operaciones_largas(parametros)
         # Si el producto esta disponible o ha bajado de precio se envia un mensaje
        if 'bajado' in resultado or 'tienes' in resultado:
            await bot.send_message(chat_id=user_id, text=f"{resultado}")
        print(resultado)
    except Exception as e:
        await bot.send_message(chat_id=user_id, text=f"Hubo un error: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())