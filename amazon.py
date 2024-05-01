import sys
import time
import asyncio
from telegram import Bot
####
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import random

from data import (TOKEN)
bot = Bot(token=TOKEN)
####

'''
Este script scrappea una web de amazon, es capaz de comprobar la disponibilidad y si se produce bajada de precio o no
Utiliza undetected_chromedriver usando un user_agent aleatorio
Responde con un valor negativo para indicar error, 0 para indicar que no ha habido cambios y un valor positivo para indicar que ha habido cambios

'''

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
        # guardamos en precio anterior el valor a continuacion del = de la cadena en un entero
        precioAnterior = float(parametro2.split('=')[1])
        # Se inicia la ventana del navegador con ventana en segundo plano
        chrome_options = webdriver.ChromeOptions()
        userAgent = agenteUsuario()
        chrome_options.add_argument(f'user-agent={userAgent}')
        chrome_options.add_argument('--headless')
        browser = uc.Chrome(options=chrome_options)
        browser.get(parametro1)
        # cookies
        try:
            WebDriverWait(browser, 10)\
                .until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sp-cc-rejectall-link"]')))\
                .click()
        except Exception as e:
            RuntimeError(f"Cookies button not found: {str(e)}")
            #browser.find_element("xpath",'//*[@id="sp-cc-rejectall-link"]').click()
        
        #refrescamos porque sale un mensaje de que hay que recargar
        #browser.refresh()
        # A veces salta que donde se encuentra el tiempo no tiene la propiedad text ... vamos a esperar por si acaso
        time.sleep(1)
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
            precio = float(precio.replace(',', '.'))
            if precioAnterior == 0:
                precioAnterior = precio
            # si ha bajado el precio notificamos
            if precio < precioAnterior:
                resultado = f"El precio ha bajado! \r\n{parametro1}"
            elif precio > precioAnterior:
                resultado = str(precio)
                #'''f"El precio ha subido! \r\n{parametro1}"'''
            else:
                resultado = str(precio)
                #'''f"El precio no ha cambiado \r\n{parametro1}"'''
            return resultado
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
                        resultado = f"La talla no está disponible \r\n{parametro1}" 
                        break       
                    else:
                        # si esta disponible
                        resultado = f"Aquí lo tienes! \r\n{parametro1}"
                        print('Talla disponible')
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
        return resultado
    except Exception as e:
        await bot.send_message(chat_id=user_id, text=f"Hubo un error: {str(e)}")
        return -1

if __name__ == '__main__':
    asyncio.run(main())