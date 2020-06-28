from functools import wraps
from telegram import ChatAction
from geopy.geocoders import GoogleV3
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
ConversationHandler)
from watson_conversation import WatsonConversation
import urllib3
import json
import pandas as pd

#Prototipo SQL
dburl = 'postgresql://postgres:123456@localhost:5432/hackathon'

q = '''SELECT description, event_data, address 
FROM violence_data
WHERE address ilike 'Rio Comprido' AND event_data BETWEEN NOW() - INTERVAL '6 HOURS' AND NOW();'''

df = pd.read_sql(q, con=dburl)

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)
        return command_func
    
    return decorator

send_typing_action = send_action(ChatAction.TYPING)

class TelegramBot(object):

    def __init__(self):
        # self.geolocator = GoogleV3("AIzaSyCZeI8Hp5aQv7rDacBxfb4DBGbmgj2yFdA")
        self.updater = Updater(token='784082052:AAF2raPeZqdY4bcRFsBOCaTJv91y2KbXbPg')
        self.watsonConversation = WatsonConversation()
        dp = self.updater.dispatcher

        # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

        start_handler = CommandHandler('start', self.start)
        dp.add_handler(start_handler)
        start_handler = CommandHandler('cancel', self.start)
        dp.add_handler(start_handler)
        echo_handler = MessageHandler(Filters.text, self.msg_handle)
        dp.add_handler(echo_handler)
        location_handler = MessageHandler(Filters.location, self.location, edited_updates=True)
        dp.add_handler(location_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def cancel(self, bot, update):
        user = update.message.from_user
        update.message.reply_text('Tchau! Espero que tenha lhe ajudado.',
                                    reply_markup=ReplyKeyboardRemove())
   
    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Olá! Sou Coruja Urbana em que posso te ajudar?")

    def msg_handle (self, bot, update):
        user = update.message.from_user
        user_text = update.message.text
        response = self.watsonConversation.get_watson_message(user_text)
        if response['intents'][0]['intent'] ==  'crime_bairro':
            import pdb; pdb.set_trace()
            bot.send_message(chat_id=update.message.chat_id,text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', parse_mode=ParseMode.HTML)
            bot.send_photo(chat_id=update.message.chat_id, photo=open('C:\\Users\\gustavo.figueiredo\\Downloads\\c2f500a638707bd8b7bb0619f4cda572.jpg', 'rb'))
        elif response['intents'][0]['intent'] ==  'ranking':
            update.message.reply_text('Ranking')
        elif response['intents'][0]['intent'] ==  'bairro':
            substring_list = ['bangu',  'barra', 'botafogo', 'campo grande', 'centro', 'copacabana', 'ilha', 'madureira', 'tijuca', 'vila']
            userText = response['input']['text'].lower()
            finalText = ''
            terms = userText.split('')
            for term in terms:
                if term in substring_list:
                    finalText = term
            print(finalText)

            #chamar SQL com  o termo recuperado aqui. Retorno vai pro update abaixo
            update.message.reply_text(finalText)
            #import pdb; pdb.set_trace()
        # print(user_text)

    def location(self, bot, update):
        http = urllib3.PoolManager()
        resultado = http.request('GET','https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(update.message.location.latitude)+','+str(update.message.location.longitude)+'&key=AIzaSyCZeI8Hp5aQv7rDacBxfb4DBGbmgj2yFdA')
        my_json = resultado.data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        update.message.reply_text( data['results'][0]['formatted_address'])

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        pass
        # logger.warning('Update "%s" caused error "%s"', update, error)


    def ML(bairro):
        
        return update.message.reply_text( 'ok')