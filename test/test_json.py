import json
import unittest

class TestJson(unittest.TestCase):
    def test_json(self):
        # obtenemos el json dle fichero
        self.file = open('test/process.txt','r')
        self.read = json.load(self.file)
        self.file.close()
        self.assertIsInstance(self.read, dict)
        self.assertEqual(self.read['name'],'test')
        self.assertEqual(self.read['dependencies']['mongoose'],'^5.9.7')
    def test_json2(self):
        self.file = open('test/process2.txt','r')
        self.read = json.load(self.file)
        self.file.close()
        self.assertIsInstance(self.read, dict, 'Helllowww')
        # recorro
        for i in self.read['actions']:
            if i['url'] ==  'https://www.elcorteingles.es/bebes/A42921137-silla-de-paseo-maxi-cosi-zelia3/?parentCategoryId=999.11852987013&color=Gris+oscuro&_gl=1*17pltrj*_up*MQ..&gclid=EAIaIQobChMImJPXp4jthQMVgDsGAB2cIAHdEAAYASAAEgIOTvD_BwE&gclsrc=aw.ds':
                self.assertEqual(i['prize'], 999.99)
                self.assertEqual(i['targetPrize'], 444.44)
                self.assertEqual(i['variation'], 10)
                self.assertEqual(i['size'], '')
                self.assertEqual(i['user'], 965741872)

        
    

def saveProcessJson():
    file = open('test/process.txt','r')
    read = json.load(file)
    file.close()
    # Abrimos el archivo para leerlo
    with open ('test/process.txt','r') as f:
        datos_json = json.load(f)
    # Leemos el archivo completo y generamos un json
    '''if f:
        # leemos todas las lineas del archivo
        lines = f.readlines()
        print(type(lines))
        strLines = str(lines)
        print(type(strLines))
        
        if len(lines) == 0:
            return
        jsonF = json.load(f)
        f.close()
        if jsonF:
            print(jsonF)
            '''


if __name__ == '__main__':
    #saveProcessJson()
    unittest.main()