import configparser
import logging

import telegram
from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

from utils import get_stock_price

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

@app.route('/index', methods=['GET'])
def index_handler():
    """get hello world when access /index."""
    return 'hello world'


def reply_handler(update: Update, context: CallbackContext):
    """Reply message."""
    text = update.message.text

    if text == 'hello':
        username = update.message.from_user.username
        if not username:
            username = str(update.message.from_user.id)
        update.message.reply_text('hello, ' + username)
    else:
        update.message.reply_text(text)

    check_price, check_name = get_stock_price(text)
    if check_price:
        update.message.reply_text(check_name + check_price)
    else:
        update.message.reply_text('error')



# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)