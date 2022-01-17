import logging
import time
from flask import Flask, request
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher, CallbackContext
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import get_reply,fetch_news,topics_keyboard


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN  = "5000353690:AAFqTA267C8Q1Yzu22fcIII2LLTQTxyvo48"

app = Flask(__name__)    #create a flask object

@app.route('/')
def index():
    return "Hello"

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():                                                      #define webhook function
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)                #create an update object, which is of Update type from telegram module and is converted from json data that webook provides
    # process update
    dp.process_update(update)
    return "ok"

def start(update, context: CallbackContext):  #/start command will run this commant with 2 arguements, update and context
    print(update)
    author = update.message.from_user.first_name
    reply = "Hi, {}".format(author)
    context.bot.send_message(chat_id = update.message.chat_id, text = reply)

def _help(update, context:CallbackContext):
    help_text = "This is a help text"
    context.bot.send_message(chat_id = update.message.chat_id, text = help_text)

def news(update, context: CallbackContext):
   bot.send_message(chat_id=update.message.chat_id, text="Choose a category", 
        reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))
        #reply markup requires a list of list or string as arguement to show up


def reply_text(update, context:CallbackContext):
    intent, reply = get_reply(update.message.text,update.message.chat_id)
    print(reply)
    if intent == "get_news":
        context.bot.send_message(chat_id = update.message.chat_id, text = "Working on it...")
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id = update.message.chat_id, text = article['link'])
            time.sleep(1)
    else:
        context.bot.send_message(chat_id = update.message.chat_id, text = reply)

def echo_sticker(update, context:CallbackContext):
    reply = update.message.text
    context.bot.send_sticker(chat_id = update.message.chat_id, sticker = update.message.sticker.file_id)
def error(update, context:CallbackContext):
    logger.error("Update '%s'caused error '%s'",update,update.error)



bot = Bot(TOKEN)                            #a bot object created with the token
try:
    bot.set_webhook("https://shob8-news-bot.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)                  #can also provide with a queue object instead of the None to keep the pending updates
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)

if __name__ == "__main__":
    # main()
    app.run(port = 8443)