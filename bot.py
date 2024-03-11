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
"""

import logging
import subprocess
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from data import (TOKEN, webSites)



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

async def ejecutar(update: Update, context: CallbackContext) -> None:

    # Obtener información del usuario y mensaje
    user_id = update.message.from_user.id
    message_text = update.message.text
    # await update.message.reply_text("Vamos a lanzar el script!")    # Lanzar el script secundario en un proceso separado

    # Puedes ajustar esta línea según tus necesidades
    parametros = " ".join(message_text.split(" ")[1:])
    found = False
    # Recorremos la lista de webs y si esta en la lista lanzamos su script
    for web in webSites:
        if web[0] in parametros:
            subprocess.Popen(['python', web[1], parametros, str(user_id)])
            await update.message.reply_text("Vamos a ello!")
            found = True
    
    if not found:
        await update.message.reply_text("No se ha encontrado la web que buscas")


    # if 'zar' in parametros:
    #    subprocess.Popen(['python', 'zara.py', parametros, str(user_id)])
    #elif 'sezane' in parametros:
    #    subprocess.Popen(['python', 'sezane.py', parametros, str(user_id)])

    # await update.message.reply_text("script lanzado!")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ejecutar", ejecutar))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()