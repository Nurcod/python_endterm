import telebot
import re
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from message_api import api
from supabase import Client,create_client
SECRET_KEY = "sb_secret_AZM7ADduXmdR_nqsTp920Q_-4TsVLuE"
PROJECT_URL = "https://ajjbldcfukrjzivigcfq.supabase.co"

supabase: Client = create_client(PROJECT_URL,SECRET_KEY)
bot = telebot.TeleBot(token='8265864879:AAF3BFmQOErTMle0ECY_HUHRu56Xrn3xfKA')
user_email = {}

@bot.message_handler(func= lambda message: message.text  and message.text.lower().strip() in ['hello','hi'])
def message_hand(message):
    bot.send_message(message.chat.id,'Hi,how are you?')
@bot.message_handler(func= lambda message: message.text and message.text.lower().strip() in ["how are you?", "how is it going?"])
def message_hand(message):
    msg = bot.send_message(message.chat.id,'I am fine,thank you,and you?')
    bot.register_next_step_handler(msg,answer)
def answer(message):
    bot.send_message(message.chat.id,'it\'s cool!')
@bot.message_handler(func=lambda message: message.text and 'thank' in message.text.lower().strip().split() and 'you' in message.text.lower().strip().split())
def answ(message):
    bot.send_message(message.chat.id,'you\'re welcome!')
@bot.message_handler(commands=['start'])
def answ(message):
    bot.send_message(message.chat.id,'Hello, I am your assistant bot, Nur Translator.\nI will help you identify the language of the text and translate it'
    '\nalso i can opportunities talk with you with help special words(hi,hello,how are you,consisting thank you in your words)'
    '\nwithout these i have functional commands,you can understand it with /info')
@bot.message_handler(commands=['info'])
def start_message(message):
    bot.send_message(message.chat.id,'\\register - registration\n\\enter - Login after registration'
    '\n\\fact\n\\joke\n\\weather')
@bot.message_handler(commands=['fact'])
def answ(message):
    bot.send_message(message.chat.id,api.chat_api.fact())
@bot.message_handler(commands=['weather'])
def answ(message):
    msg = bot.send_message(message.chat.id,'Your city:')
    bot.register_next_step_handler(msg,weath)
def weath(message):
    text = message.text.capitalize()
    arr = api.chat_api.weather(text)
    bot.send_message(message.chat.id,f"{text}\nWeather: {arr[0]}\nTemp: {arr[1]}\nWind speed: {arr[2]}\nWind degree: {arr[3]}")
@bot.message_handler(commands=['joke'])
def jokee(message):
    bot.send_message(message.chat.id,api.chat_api.joke())
@bot.message_handler(commands=['register'])
def register(message):
    msg = bot.send_message(message.chat.id,'email:')
    bot.register_next_step_handler(msg,get_email)
def get_email(message):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Please write your email correctly:')
        bot.register_next_step_handler(msg,get_email)
    else:
        try:
            email = supabase.table('users').select('email','password').eq('email',message.text).execute().data
            if email:
                if email[0]['password'] == None:
                    msg = bot.send_message(message.chat.id,'Write your password (length 8 characters, 1 capital letter, number and special character):')
                    user_email[f"{message.chat.id}"] = {}
                    user_email[f"{message.chat.id}"]['email'] = message.text
                    bot.register_next_step_handler(msg,get_password)
                    
                else:
                    bot.send_message(message.chat.id,'A user with this email is already registered!')
            else:
                supabase.table('users').insert({'email':message.text}).execute()
                user_email[f"{message.chat.id}"] = {}
                user_email[f"{message.chat.id}"]['email'] = message.text
                msg = bot.send_message(message.chat.id,'Write your password (length 8 characters, 1 capital letter, number and special character):')
                bot.register_next_step_handler(msg,get_password)
        except:
            msg = bot.send_message(message.chat.id,'An error occurred, please enter your email again:')
            bot.register_next_step_handler(msg,get_email)

def get_password(message):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    if  bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Please enter your password correctly (8 characters long, 1 capital letter, 1 number and special character):')
        bot.register_next_step_handler(msg,get_password)
    else:
        try:
            supabase.table('users').update({'password': message.text}).eq('email',user_email[f"{message.chat.id}"]['email']).execute()
            bot.send_message(message.chat.id,'Registration completed successfully')
        except:
            msg = bot.send_message(message.chat.id,'An error occurred, please enter your password again:')
            bot.register_next_step_handler(msg,get_password)
@bot.message_handler(commands=['enter'])
def enter(message):
    
    msg = bot.send_message(message.chat.id,'email:')
    bot.register_next_step_handler(msg,observe_email)
def observe_email(message):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Please write your email correctly:')
        bot.register_next_step_handler(msg,observe_email)
    try:
        email = supabase.table('users').select('email').eq('email',message.text).execute().data
        user_email[f"{message.chat.id}"] = {}
        user_email[f"{message.chat.id}"]['email'] = message.text
        if email:
            msg = bot.send_message(message.chat.id,'Write your password (length 8 characters, 1 capital letter, number and special character):')
            bot.register_next_step_handler(msg,observe_password)
        else:
            bot.send_message(message.chat.id,'Email is incorrect, try logging in again.')
    except Exception as e:
        msg = bot.send_message(message.chat.id,'A technical error occurred, please enter your email again:')
        print(e)
        bot.register_next_step_handler(msg,observe_email)
def observe_password(message):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    if  bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Please enter your password correctly (8 characters long, 1 capital letter, 1 number and special character):')
        bot.register_next_step_handler(msg,observe_password)
    try:
        if supabase.table('users').select('password').eq('email',user_email[f"{message.chat.id}"]['email']).execute().data[0]['password'] == message.text:
            bot.send_message(message.chat.id,'Login successfully completed!')
            msg = bot.send_message(message.chat.id,'Enter a word to define (0-exit):')
            bot.register_next_step_handler(msg,chat)
        else:
            bot.send_message(message.chat.id,'Incorrect password, try logging in again:')
    except:
        msg = bot.send_message(message.chat.id,'A technical error occurred. Please enter your password again:')
        bot.register_next_step_handler(msg,observe_password)
def chat(message):
    supabase.table('translate_data').insert({'login':user_email[f"{message.chat.id}"]['email'],'text': message.text}).execute()
    if message.text == '0':
        bot.send_message(message.chat.id,'You have successfully logged out')
        return
    chat_api = api.chat_api
    response  = chat_api.send_message(message.text)
    if response == []:
        bot.send_message(message.chat.id,'Just words please')
        msg = bot.send_message(message.chat.id,'Enter a word to define (0-exit):')
        bot.register_next_step_handler(msg,chat)
    else:
        msg = bot.send_message(message.chat.id,f"language: {response[0]}\nTranslation:{response[1]}")
        msg = bot.send_message(message.chat.id,'Enter a word to define (0-exit):')
        bot.register_next_step_handler(msg,chat)
@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.reply_to(message, "Hello, you entered an incorrect command or message. Type /start to view the information.")

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), BaseHTTPRequestHandler)
    server.serve_forever()
threading.Thread(target=run_server).start()


bot.infinity_polling(skip_pending=True)


