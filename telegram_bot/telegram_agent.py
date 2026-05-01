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
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Здравствуйте я ваш бот помощник Nur Translator\nя помогу вам определить язык текста и перевести его но сначало зарегистрируйтесь' \
    '\n\\register - регистрация\n\\enter - вход после регистраций')
@bot.message_handler(commands=['register'])
def register(message):
    msg = bot.send_message(message.chat.id,'Пишите ваш email:')
    bot.register_next_step_handler(msg,get_email)
def get_email(message):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Напишите email корректно:')
        bot.register_next_step_handler(msg,get_email)
    else:
        try:
            email = supabase.table('users').select('email','password').eq('email',message.text).execute().data
            if email:
                if email[0]['password'] == None:
                    msg = bot.send_message(message.chat.id,'Пишите ваш пароль(длина 8 символов,1 Большая буква,цифра и спец символ):')
                    user_email['email'] = message.text
                    bot.register_next_step_handler(msg,get_password)
                    
                else:
                    bot.send_message(message.chat.id,'Пользователь с  таким email уже зарегистрирован!')
            else:
                supabase.table('users').insert({'email':message.text}).execute()
                user_email['email'] = message.text
                msg = bot.send_message(message.chat.id,'Пишите ваш пароль(длина 8 символов,1 Большая буква,цифра и спец символ):')
                bot.register_next_step_handler(msg,get_password)
        except:
            msg = bot.send_message(message.chat.id,'Случилась ошибка напишите email еще раз:')
            bot.register_next_step_handler(msg,get_email)

def get_password(message):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    if  bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Напишите пароль корректно(длина 8 символов,1 Большая буква,цифра и спец символ):')
        bot.register_next_step_handler(msg,get_password)
    else:
        try:
            supabase.table('users').update({'password': message.text}).eq('email',user_email['email']).execute()
            bot.send_message(message.chat.id,'Регистрация успешно завершена')
        except:
            msg = bot.send_message(message.chat.id,'Случилась ошибка напишите пароль еще раз:')
            bot.register_next_step_handler(msg,get_password)
@bot.message_handler(commands=['enter'])
def enter(message):
    msg = bot.send_message(message.chat.id,'Напишите ваш email')
    bot.register_next_step_handler(msg,observe_email)
def observe_email(message):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Напишите email корректно:')
        bot.register_next_step_handler(msg,observe_email)
    try:
        email = supabase.table('users').select('email').eq('email',message.text).execute().data
        user_email['email'] = message.text
        if email:
            msg = bot.send_message(message.chat.id,'Пишите ваш пароль(длина 8 символов,1 Большая буква,цифра и спец символ):')
            bot.register_next_step_handler(msg,observe_password)
        else:
            bot.send_message(message.chat.id,'Email неверный попробуйте войти еще раз')
    except:
        msg = bot.send_message(message.chat.id,'Случилась тех ошибка,введите email еще раз')
        bot.register_next_step_handler(msg,get_email)
def observe_password(message):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    if  bool(re.match(pattern, message.text)) == 0:
        msg = bot.send_message(message.chat.id,'Напишите пароль корректно(длина 8 символов,1 Большая буква,цифра и спец символ):')
        bot.register_next_step_handler(msg,observe_password)
    try:
        if supabase.table('users').select('password').eq('email',user_email['email']).execute().data[0]['password'] == message.text:
            bot.send_message(message.chat.id,'Вход успешно оформлен!')
            msg = bot.send_message(message.chat.id,'Введите слово для определения(0-выход):')
            bot.register_next_step_handler(msg,chat)
        else:
            bot.send_message(message.chat.id,'Неверный пароль попробуйте еще раз войти')
    except:
        msg = bot.send_message(message.chat.id,'Случилась тех ошибка введите пароль еще раз')
        bot.register_next_step_handler(msg,get_password)
def chat(message):
    if message.text == '0':
        bot.send_message(message.chat.id,'Вы успешно вышли')
        return
    chat_api = api.chat_api
    response  = chat_api.send_message(message.text)
    if response == []:
        bot.send_message(message.chat.id,'Только слова пожалуйста')
        msg = bot.send_message(message.chat.id,'Введите слово для определения(0-выход):')
        bot.register_next_step_handler(msg,chat)
    else:
        msg = bot.send_message(message.chat.id,f"язык: {response[0]}\nПеревод:{response[1]}")
        msg = bot.send_message(message.chat.id,'Введите слово для определения(0-выход):')
        bot.register_next_step_handler(msg,chat)

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), BaseHTTPRequestHandler)
    server.serve_forever()
threading.Thread(target=run_server).start()
bot.polling(none_stop=True)


