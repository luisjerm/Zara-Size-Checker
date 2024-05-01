#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
Notes:
- Usamos esto en la libreria de undetected chromedriver porque al cerrarlo con .quit() peta, modificamos el metodo __del__
    https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/955

"""
import os
import logging
import subprocess
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from data import (TOKEN, webSites)
import threading as th
import time, random 

# create a lock
lock = th.Lock()
# acquire the lock
lock.acquire()
lock.release()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

# realiza una espera aleatoria 
def timepoAleatorio(val):
    min = 300
    max = 600
    ranges = [i for i in range(min, max)]
    delay = random.choice(ranges)
    print(delay)
    return delay

def saveProcess(params, user):
    # bloqueo el proceso 
    lock.acquire()
    f = open ('process.txt','a')
    # Recorremos la lista de webs y si esta en la lista lanzamos su script
    found = False
    for web in webSites:
        if web[0] in params:
            #  A parte hay que comprobar mas cosas, para segurarnos que no nos meten  mierda 
            f.write(params + ' ' + user + '\n')
            print('Guardado '+ params)
            f.close()
            found = True
            break
    lock.release()
    return found

def executeProcess():
    # bloqueo el proceso 
    lock.acquire()
    if os.path.isfile('process.txt') == False:
        lock.release()
        return
    f = open ('process.txt','r')
    if f:
        # leemos todas las lineas del archivo
        lines = f.readlines()
        lines_new = lines.copy()
        f.close()
        if len(lines) == 0:
            lock.release()
            return
        # recorremos las lineas
        for line in lines:
            print('Linea '+ line)
            # dividimos la linea en 3 partes
            att = line.split()
            user = att[-1]
            url = att[0]
            params = ' '.join(att[1:-1])
            parametros = url + ' ' + params
            # Recorremos la lista de webs y si esta en la lista lanzamos su script
            for web in webSites:
                if web[0] in url:
                    # lanzamos el proceso
                    script = subprocess.Popen(['python', web[1], parametros, user], stdout=subprocess.PIPE)
                    output = script.communicate()[0].decode()
                    # esperamos a que termine
                    script.wait()
                    output = output.replace('\r\n', '')
                    print('Proceso terminado: ' + output + 'longitud:' + str(len(output)))
                    if output == -1:
                        print('Error en el script')
                    else:
                        if len(output) == 0:
                            print('Resultado vacio')
                            continue
                        print('Proceso terminado')
                        if 'bajado' in output or 'tienes' in output:
                            # borramos la linea del archivo
                            lines_new.remove(line)
                        else:
                            # si en line aparece precio= actalizamos el valor que aparece despues del = hasta el espacio con el valor de output
                            if 'precio=' in line:
                                lines_new.remove(line)
                                updPrize = params.split('=')[0]
                                # revisar cuando hay size y precio, hay que mantener el size¡¡¡¡¡¡¡¡
                                line = url + ' ' + updPrize + '=' + output + ' ' + user + '\n'
                                lines_new.append(line)
        # escribimos las lineas en el archivo
        # borramos el archivo
        os.remove('process.txt')
        f = open ('process.txt','w')
        for line in lines_new:
            f.write(line)
        f.close()


    lock.release()

async def talla(update: Update, context: CallbackContext) -> None:

    # Obtener información del usuario y mensaje
    user_id = update.message.from_user.id
    message_text = update.message.text
    # await update.message.reply_text("Vamos a lanzar el script!")    # Lanzar el script secundario en un proceso separado

    # Puedes ajustar esta línea según tus necesidades
    parametros = " ".join(message_text.split(" ")[1:])
    found = saveProcess(parametros, str(user_id))
    # Recorremos la lista de webs y si esta en la lista lanzamos su script
    '''for web in webSites:
        if web[0] in parametros:
            subprocess.Popen(['python', web[1], parametros, str(user_id)])
            await update.message.reply_text("Vamos a ello!")
            found = True'''
    
    if not found:
        await update.message.reply_text("No se ha encontrado la web que buscas")
        
async def precio(update: Update, context: CallbackContext) -> None:

    # Obtener información del usuario y mensaje
    user_id = update.message.from_user.id
    message_text = update.message.text
    # await update.message.reply_text("Vamos a lanzar el script!")    # Lanzar el script secundario en un proceso separado

    # Puedes ajustar esta línea según tus necesidades
    parametros = " ".join(message_text.split(" ")[1:])
    #insertamos el parametro precio con valor 0
    parametros = parametros + " precio=0"
    found = saveProcess(parametros, str(user_id))
    # Recorremos la lista de webs y si esta en la lista lanzamos su script
    '''for web in webSites:
        if web[0] in parametros:
            subprocess.Popen(['python', web[1], parametros, str(user_id)])
            await update.message.reply_text("Vamos a ello!")
            found = True'''
    
    if not found:
        await update.message.reply_text("No se ha encontrado la web que buscas")

async def TallaPrecio(update: Update, context: CallbackContext) -> None:

    # Obtener información del usuario y mensaje
    user_id = update.message.from_user.id
    message_text = update.message.text
    # await update.message.reply_text("Vamos a lanzar el script!")    # Lanzar el script secundario en un proceso separado

    # Puedes ajustar esta línea según tus necesidades
    parametros = " ".join(message_text.split(" ")[1:])
    parametros = parametros + " precio"
    found = saveProcess(parametros, str(user_id))
    # Recorremos la lista de webs y si esta en la lista lanzamos su script
    '''for web in webSites:
        if web[0] in parametros:
            # guardamos el proceso en archivo

            subprocess.Popen(['python', web[1], parametros, str(user_id)])
            await update.message.reply_text("Vamos a ello!")
            found = True'''
    
    if not found:
        await update.message.reply_text("No se ha encontrado la web que buscas")

def processCheckTh():
    while True:
        wait = timepoAleatorio(20)
        waitIter = wait/0.1
        for i in range(0, int(waitIter)):
            # duerme el hilo
            time.sleep(0.1)
        executeProcess()

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("talla", talla))
    application.add_handler(CommandHandler("precio", precio))
    application.add_handler(CommandHandler("tp", TallaPrecio))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Creamos un hilo
    th.Thread(target=processCheckTh).start()
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # cerramos el hilo
    th.Thread(target=processCheckTh).join()

if __name__ == "__main__":
    main()