
''' 
Esta clase nos permite scrappear una página web mediante el uso de Selenium y chromedriver


'''
from selenium import webdriver
from selenium.webdriver.common.by import By
# esperas para que aparezcan elementos en la web
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import random


class WebScrapper:
     # eleccion aletoria de user agent
    def agenteUsuario(self):
        with open('user_agents.txt') as f:
            user_agents = f.read().split("\n")
            return random.choice(user_agents)
        
    def __init__(self, headless = False):
        self.chrome_options = webdriver.ChromeOptions()
        userAgent = self.agenteUsuario()
        self.chrome_options.add_argument(f'user-agent={userAgent}')
        if headless:
            self.chrome_options.add_argument('--headless')
        
    def quit(self):
        self.browser.close()
        self.browser.quit()

    def getPage(self, url):
        self.browser = uc.Chrome(options=self.chrome_options)
        self.browser.get(url)

    def acceptCookies(self, path, timeout = 10):    
        try:
            WebDriverWait(self.browser, timeout)\
                .until(EC.element_to_be_clickable((By.XPATH, path)))\
                .click()
        except Exception as e:
            return False
            #RuntimeError(f"Cookies button not found: {str(e)}")
        return True

    def getElem(self, elem):
        try:
            return self.browser.find_element(By.CSS_SELECTOR, elem)
        except Exception as e:
            # print(f"Element{str(elem)} not found: {str(e)}")
            return False
    
    def getElements(self, elem):
        try:
            return self.browser.find_elements(By.CSS_SELECTOR, elem)
        except Exception as e:
            # print(f"Elements{str(elem)} not found: {str(e)}")
            return False
    
    '''
        Busca dentro de container un elemento con el texto text y lo clickea
    '''
    def searchAndClickTextElemInContainer(self, container, elem, text):
        try:
            for i in self.browser.find_elements(By.CSS_SELECTOR, container):
                if text in i.find_element(By.CSS_SELECTOR, elem).text:
                    i.click()
                    return True
            return False
        except Exception as e:
            #print(f"Element{str(elem)} in container {str(container)} not found: {str(e)}")
            return False

        
    def getElemText(self, elem):
        try:
            res = self.browser.find_element(By.CSS_SELECTOR, elem).text
            return res
        except Exception as e:
            #print(f"Element{str(elem)} text not found: {str(e)}")
            return False
        
    def clickElem(self, elem, type = 'css', timeout = 5):
        try:
            if type == 'css':
                WebDriverWait(self.browser, timeout)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR, elem)))\
                .click()
            elif type == 'xpath':
                WebDriverWait(self.browser, timeout)\
                .until(EC.element_to_be_clickable((By.XPATH, elem)))\
                .click()
            else:
                print(f'Invalid type: {type}')
                return False
            return True
        except Exception as e:
            #print(f"Element{str(elem)} not found in {str(timeout)}s: {str(e)}")
            return False
        
    def clickElemByXpath(self, elem, timeout = 5):
        return self.clickElem(elem, 'xpath', timeout)
    
    def clickElemByCSS(self, elem, timeout = 5):
        return self.clickElem(elem, 'css', timeout)
    
    def setContainerName(self, container):
        self.container = container

    def getContainer(self):
        return self.browser.find_element(By.CSS_SELECTOR, self.container)

    def setElemContainerName(self, elemContainer):
        self.elemContainer = elemContainer

    def setElemLabelSize(self, elemLabelSize):
        # seteamos el label del elemento que contiene la talla
        self.elemLabelSize = elemLabelSize

    def getElemLabelSize(self, elem):
        return elem.find_element(By.CSS_SELECTOR, self.elemLabelSize).text
    
    def setElemLabelPrize(self, elemLabelPrize):
        # seteamos el label del elemento que contiene el precio
        self.elemLabelPrize = elemLabelPrize

    def getElemLabelPrize(self):
        return self.browser.find_element(By.CSS_SELECTOR, self.elemLabelPrize).text
    
    def setDropDownAndExpand(self, dropDown, timeout = 5):
        # desplegamos el dropdown
        WebDriverWait(self.browser, timeout)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, dropDown)))\
            .click()
        
    def getButtonText(self, button, text):
        # Encontrar todos los elementos que son botones
        botones = self.browser.find_elements(By.CSS_SELECTOR, 'button')

        # Verificar si alguno de los botones tiene el texto "agotado"
        boton_agotado = False
        for boton in botones:
            text_button = boton.text.lower()
            if text_button == "agotado":
                boton_agotado = True
                break
        return boton_agotado


if __name__ == '__main__':
    web = WebScrapper()
    web.getPage('https://www.elcorteingles.es/bebes/A42921137-silla-de-paseo-maxi-cosi-zelia3/?parentCategoryId=999.11852987013&color=Gris+oscuro&_gl=1*17pltrj*_up*MQ..&gclid=EAIaIQobChMImJPXp4jthQMVgDsGAB2cIAHdEAAYASAAEgIOTvD_BwE&gclsrc=aw.ds')
    web.acceptCookies('//*[@id="onetrust-accept-btn-handler"]')
    web.setElemLabelPrize('span.price-unit--normal.product-detail-price')
    prize = web.getElemLabelPrize()
    print("Precio: " + prize)
    web.quit()