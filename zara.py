import sys
import time
import asyncio
from telegram import Bot
####
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import winsound
from data import (TOKEN)
####

bot = Bot(token=TOKEN)



async def operaciones_largas(parametros):
    try:
        # Dividir los parámetros en dos strings
        parametro1, parametro2 = parametros.split()

        # evitamos abrir la ventana del navegador
        options = Options()
        options.add_argument('--headless')
        #options.headless = True

        # Se inicia la ventana del navegador options=options,
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

        # Se escribe el link al artículo
        # driver.get('https://www.zara.com/es/es/share/-p05427407.html?v1=327249367&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil')
        driver.get(parametro1)

        # Se escribe la talla que se quiere
        talla_elegida = parametro2 # 'm'

        try:
            while 1:
                # El bloque de las tallas se ubica dentro de un elemento <ul> por lo tanto se busca que ese elemento contenga el id que se quiere
                ul_element = driver.find_element(By.CSS_SELECTOR, 'ul[id*="product-size-selector"]')

                # Se traen los bloques de elementos li que son los de las tallas
                li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                
                # Recorremos li_elements y buscamos dentro de los atributos de cada elemento el que contenga la talla que queremos
                for i in range(len(li_elements)):
                    # Se guarda el elemento que corresponda a la talla seleccionada
                    talla = li_elements[i]
                    # si es nuestra talla
                    if talla_elegida.upper() in talla.accessible_name:
                        # Se guarda el atributo <class> que indica si está fuera de stock o no
                        class_name = talla.get_attribute('class')
                
                        # Si no aparece el texto out-of-stock significa que hay talla
                        if "out-of-stock" not in class_name:
                            resultado = f"Operaciones completadas con parámetros: {parametro1}"
                            return resultado
                            for i in range(10):
                                # Imprime 10 veces el texto
                                print("TALLA " + talla_elegida.upper() + " DISPONIBLE")

                                # Se reproducen 10 pitidos
                                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                        else:
                            # Se duerme al proceso x segundos   
                            await asyncio.sleep(20) 
                            break       
                            #time.sleep(20)

                # Se actualiza la página
                print("------- Actualizando web -------- \n")
                await driver.refresh()


        except NoSuchElementException as e:
            print("No se encontró el elemento " + str(e))
        # Realizar operaciones de larga duración
        # await asyncio.sleep(10)  # Simulación de operaciones de larga duración
        resultado = f"Operaciones completadas con parámetros: {parametro1}"
        return resultado
    except Exception as e:
        raise RuntimeError(f"Error en operaciones_largas: {str(e)}")

async def main():
    parametros = sys.argv[1]
    user_id = sys.argv[2]

    try:
        resultado = await operaciones_largas(parametros)
        await bot.send_message(chat_id=user_id, text=f"¡Operaciones completadas!\n\n{resultado}")
    except Exception as e:
        await bot.send_message(chat_id=user_id, text=f"Hubo un error: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())