import random

# realiza una espera aleatoria 
def timepoAleatorio(val):
    ranges = [i for i in range(3, val+1)]
    return random.choice(ranges)

# eleccion aletoria de user agent
def agenteUsuario():
    with open('user_agents.txt') as f:
        user_agents = f.read().split("\n")
        return random.choice(user_agents)


def createEntry():
    entry = {
                'url': '' ,\
                'prizeInfo': {\
                    'initialPrize': -1,\
                    'prize': -1,\
                    'targetPrize': 0,\
                    'discount': 0,\
                    'checkPrize': False, \
                },\
                'size': '',\
                'user': 0,\
                'notify': False\
            }
    return entry

def createEntry(params, user):
    entry = createEntry()
    att = params.split()
    for i in range(0, len(att)):
        if i == 0:
            entry['url'] = att[i]
            continue
        if 'precio' in att[i]:
            entry['prizeInfo']['targetPrize'] = float(att[i].split('=')[1])
            entry['prizeInfo']['checkPrize'] = True
        elif 'discount' in att[i]:
            entry['prizeInfo']['discount'] = float(att[i].split('=')[1])
            entry['prizeInfo']['checkPrize'] = True
        elif 'talla' in att[i]:
            entry['size'] = att[i].split('=')[1]
        else:
            print('Parametro no reconocido: ' + att[i])
            return
        
    entry['user'] = user
    entry['notify'] = False
    return entry

def updateEntry(entry, precio, precioInicial, notify):
    entry['prizeInfo']['prize'] = precio
    entry['prizeInfo']['initialPrize'] = precioInicial
    entry['notify'] = notify
    return entry

def checkPrize(precio, precioInicial, variacion, precioObjt):
    # Si cehqueamos unicamente que baje de precio
    if variacion == 0 and precioObjt == 0:
        if precio < precioInicial:
            return True
        else:
            return False
    # Si chequeamos que baje un porcentaje
    elif variacion != 0 and precioObjt == 0:
        if precio <= precioInicial * (1 - variacion/100):
            return True
        else:
            return False
    # Si chequeamos que baje a un precio objetivo
    elif variacion == 0 and precioObjt != 0:
        if precio <= precioObjt:
            return True
        else:
            return False
    else:
        return False


def check(talla, tallDisp, precio, precioInicial, variacion, precioObjt):
    # No comprobamos talla
    if talla == '':
        return checkPrize(precio, precioInicial, variacion, precioObjt)
    else:
        if talla != '' and tallDisp == True:
            return checkPrize(precio, precioInicial, variacion, precioObjt)
        else:
            return False
        
def parsePrize(prize):
    prize = prize.replace('€', '')
    # Quitamos espacios
    prize = prize.strip()
    # Si supera los 1000€ puede llevar punto para los millares y coma para los decimales
    prize = float(prize.replace('.', '').replace(',', '.'))
    return prize

'''
    Evaluamos el estado de la solicitud y el estado actual del producto para detectar que condición es la que se ha cumplido
    y generar un mensaje de respuesta
'''
def createResponseMsg(data):
    # Podemos chequear por precio, talla o ambas
    if data['prizeInfo']['checkPrize'] == True:
        if data['size'] != '':
            if data['notify'] == True:
                if data['prizeInfo']['variation'] == 0 and data['prizeInfo']['targetPrize'] == 0:
                    return f"El producto ha bajado de precio de {data['prizeInfo']['initialPrize']} a {data['prizeInfo']['prize']}€ y la talla {data['size']} está disponible"
                elif data['prizeInfo']['variation'] != 0:
                    return f"El producto ha bajado un {data['prizeInfo']['variation']}% de precio a {data['prizeInfo']['prize']}€ y la talla {data['size']} está disponible"
                elif data['prizeInfo']['targetPrize'] != 0:
                    return f"El producto ha bajado de precio de {str(data['prizeInfo']['initialPrize']).replace('.',',')}€ a *{str(data['prizeInfo']['prize']).replace('.',',')}€*  💪 y la talla {data['size']} está disponible"
            else:
                return f"El producto no ha bajado de precio y la talla {data['size']} no está disponible"
        else:
            if data['notify'] == True:
                if data['prizeInfo']['variation'] == 0 and data['prizeInfo']['targetPrize'] == 0:
                    return f"El producto ha bajado de precio de {data['prizeInfo']['initialPrize']} a {data['prizeInfo']['prize']}€"
                elif data['prizeInfo']['variation'] != 0:
                    return f"El producto ha bajado un {data['prizeInfo']['variation']}% de precio a {data['prizeInfo']['prize']}€"
                elif data['prizeInfo']['targetPrize'] != 0:
                    return f"El producto ha bajado de precio de {data['prizeInfo']['initialPrize']} a {data['prizeInfo']['prize']}€"
            else:
                return f"El producto no ha bajado de precio"
    else:
        if data['size'] != '':
            if data['notify'] == True:
                return f"La talla {data['size']} está disponible"
            else:
                return f"La talla {data['size']} no está disponible"
        else:
            return f"El producto no ha bajado de precio y la talla no está disponible"
    


        
        
