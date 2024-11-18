import unittest
#from ...utils import *
from WebScrapper import WebScrapper

class TestWebScrapper(unittest.TestCase):
    #url = 'https://www.elcorteingles.es/bebes/A42921137-silla-de-paseo-maxi-cosi-zelia3/?parentCategoryId=999.11852987013&color=Gris+oscuro&_gl=1*17pltrj*_up*MQ..&gclid=EAIaIQobChMImJPXp4jthQMVgDsGAB2cIAHdEAAYASAAEgIOTvD_BwE&gclsrc=aw.ds'
    url = 'https://www.elcorteingles.es/electronica/A50060839-portatil-asus-zenbook-14-oled-ux3405ma-pz076w-intel-core-ultra-7-evo-edition-16gb-1tb-ssd-14-w11/?parentCategoryId=997.46358888011&color=Plata'
    cookies = '//*[@id="onetrust-accept-btn-handler"]'
    prizeLabel = 'span.price-unit--normal.product-detail-price'
    precioActual = 360

    @classmethod
    def setUpClass(cls):
        cls.webScrapper = WebScrapper()

    '''def test_1(self):
        self.webScrapper = WebScrapper()
        self.assertIsInstance(self.webScrapper, WebScrapper)'''

    def test_2(self):
        self.webScrapper.getPage(self.url)
        
    def test_3(self):
        # res = self.webScrapper.acceptCookies(self.cookies, 10)
        res = self.webScrapper.clickElem('//*[@id="onetrust-accept-btn-handler"]','xpath', 10)
        self.assertTrue(res)

    def test_4(self):
        '''self.webScrapper.setElemLabelPrize('span.price-unit--normal.product-detail-price')
        prize = self.webScrapper.getElemLabelPrize()'''
        # Precio sin ofertas
        prize = self.webScrapper.getElemText('span.price-unit--normal.product-detail-price')
        if prize == False:
            # precio actual con rebaja. Aparece texto del precio actual, anterior y porcentaje de descuento
            prize = self.webScrapper.getElemText('span.price-sale')
        self.assertEqual(self.parsePrize(prize), self.precioActual)

    def test_5(self):
        self.webScrapper.quit()

    @staticmethod
    def parsePrize(prize):
        prize = prize.replace('€', '')
        # Quitamos espacios
        prize = prize.strip()
        prize = float(prize.replace(',', '.'))
        return prize


if __name__ == '__main__':
    unittest.main()
