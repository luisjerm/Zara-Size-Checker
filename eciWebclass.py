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
        browser = WebScrapper()
        res = browser.getPage(url)
        # cookies, subimos tiempo, antes 5s saltaba error porque tenian cuenta atras
        res = browser.clickElemByXpath('//*[@id="onetrust-reject-all-handler"]', timeout=30)
        found = True
        if(talla != ''):
            # desplegamos tamanos
            res = browser.clickElemByCSS('div.dropdown-input', 5)
            # evaluamos si existe el tamaño indicado
            found = browser.searchAndClickTextElemInContainer('div.size-element__container', 'span.size-label', talla)
        if found:
            # evaluamos el precio
            precioValor = browser.getElemText('span.price-unit--normal.product-detail-price')
            if precioValor == False:
                # precio actual con rebaja. Aparece texto del precio actual, anterior y porcentaje de descuento
                precioValor = browser.getElemText('span.price-sale')
                precioSinOferta = browser.getElemText('span.price-unit--original.product-detail-price')
                descuento = browser.getElemText('span.price-discount')
                if precioValor == False:
                    # Evaluamos si esta disponible
                    agotado = browser.getButtonText('button', 'agotado')

        
        browser.quit()
        
        if checkPrize == True:
            precioValor = parsePrize(precioValor)
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
        print(resultado)
    except Exception as e:
        print(f"Hubo un error {str(frameinfo)}: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())