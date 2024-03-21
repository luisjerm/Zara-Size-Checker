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
        # Aceptamos cooquiesz
        WebDriverWait(browser, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))\
            .click()
        #browser.find_element("xpath",'//*[@id="onetrust-accept-btn-handler"]').click()
        html = browser.page_source
        soup = bs(html, 'html.parser')
        #browser.close()
        browser.quit()
        
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
    user_id = sys.argv[2]

    try:
        resultado = await operaciones_largas(parametros)
        # Si el producto esta disponible o ha bajado de precio se envia un mensaje
        if 'bajado' in resultado or 'tienes' in resultado:
            await bot.send_message(chat_id=user_id, text=f"{resultado}")
        print(resultado)
    except Exception as e:
        await bot.send_message(chat_id=user_id, text=f"Hubo un error: {str(e)}")
        print('-1')
        return -1

if __name__ == '__main__':
    asyncio.run(main())