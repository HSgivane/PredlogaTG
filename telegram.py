import telebot, sqlite3, os
from telebot import types
from config import *
from database import *
from date import *
from random import randint
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot=telebot.TeleBot(TOKEN)


def sms_pred(tg_name, photo_id, text):
    sms = f'Предложение от: @{tg_name}\nАйди фото: {photo_id}\n\n{text}'
    return sms


def start_key():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Предложить идею для прикола")
    btn2 = types.KeyboardButton("Предложить мем")
    btn3 = types.KeyboardButton("Панель админа")
    return markup.add(btn1, btn2, btn3)


def adm_key():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Предложенные идеи")
    btn2 = types.KeyboardButton("Предложенные мемы")
    btn3 = types.KeyboardButton("Назад")
    return markup.add(btn1, btn2, btn3)


def idea_key():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Следующая идея")
    btn2 = types.KeyboardButton("Забанить автора идеи")
    btn3 = types.KeyboardButton("Назад")
    return markup.add(btn1, btn2, btn3)


def mem_key():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Следующий мем")
    btn2 = types.KeyboardButton("Забанить автора мема")
    btn3 = types.KeyboardButton("Назад")
    return markup.add(btn1, btn2, btn3)


@bot.message_handler(commands=['start'])
def start(message):
    con = sqlite3.connect("tg.db")
    cur = con.cursor()
    user_id = message.from_user.id
    tg_name = str(message.from_user.username)
    db_tgid(user_id, tg_name, cur, con)
    markup = start_key()
    bot.send_message(message.chat.id, start_msg, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    con = sqlite3.connect("tg.db")
    cur = con.cursor()    
    user_id = message.from_user.id    
    if message.text == adm_pass:
        db_tgadm(user_id, cur, con) 
        bot.send_message(user_id, 'Поздравляю! Теперь вы героиновый черт!')
        
    elif message.text == adm_panel:
        if db_admcheck(user_id, cur, con) == True:
            markup = adm_key()
            bot.send_message(message.chat.id, admiral, reply_markup=markup)
        else:
            bot.send_message(user_id, 'У тебя недостаточно прав.')
    
    elif message.text == 'Забанить автора идеи':
        if db_admcheck(user_id, cur, con) == True:
            if db_lastidea(2, cur, con) == False:
                bot.send_message(user_id, 'Некого банить, братишка.')
            else:
                last_tg, last_id = db_lastidea(1, cur, con)
                db_tgban(last_tg, cur, con)
                bot.send_message(user_id, 'Автор идеи забанен.') 
        else:
            bot.send_message(user_id, 'У тебя недостаточно прав.')        
    
    elif message.text == 'Забанить автора мема':
        if db_admcheck(user_id, cur, con) == True:
            if db_lastidea(2, cur, con) == False:
                bot.send_message(user_id, 'Некого банить, братишка.')
            else:
                last_tg, last_id = db_lastidea(2, cur, con)
                db_tgban(last_tg, cur, con)
                bot.send_message(user_id, 'Автор мема забанен.') 
        else:
            bot.send_message(user_id, 'У тебя недостаточно прав.')    
    
    elif message.text == 'Следующая идея':
        if db_admcheck(user_id, cur, con) == True:
            if db_lastidea(1, cur, con) == False:
                bot.send_message(user_id, 'Предложенных идей больше нет.')
            else:
                last_tg, last_id = db_lastidea(1, cur, con)
                db_delete(last_id, cur, con)
                try:
                    os.remove(f"mems/{last_id}.png")
                except:
                    a = 1
                con = sqlite3.connect("tg.db")
                cur = con.cursor()            
                if db_lastidea(1, cur, con) == False:
                    bot.send_message(user_id, 'Предложенных идей больше нет.')
                else:                 
                    tg_name, photo_id, text, primary_id = db_takeidea(1, cur, con)
                    sms = sms_pred(tg_name, photo_id, text)
                    if photo_id == 'None':
                        bot.send_message(message.chat.id, sms)
                    else:
                        bot.send_photo(message.chat.id, open(f"mems/{photo_id}.png", 'rb'), sms)                
        else:
            bot.send_message(user_id, 'У тебя недостаточно прав.')        
    
    elif message.text == 'Следующий мем':
        if db_admcheck(user_id, cur, con) == True:
            if db_lastidea(2, cur, con) == False:
                bot.send_message(user_id, 'Предложенных мемов больше нет.')
            else:
                last_tg, last_id = db_lastidea(2, cur, con)
                db_delete(last_id, cur, con)
                os.remove(f"mems/{last_id}.png")
                con = sqlite3.connect("tg.db")
                cur = con.cursor()                
                if db_lastidea(2, cur, con) == False:
                    bot.send_message(user_id, 'Предложенных мемов больше нет.')
                else:               
                    tg_name, photo_id, text, primary_id = db_takeidea(2, cur, con)
                    sms = sms_pred(tg_name, photo_id, text)
                    if photo_id == 'None':
                        bot.send_message(message.chat.id, sms)
                    else:
                        bot.send_photo(message.chat.id, open(f"mems/{photo_id}.png", 'rb'), sms)                
        else:
            bot.send_message(user_id, 'У тебя недостаточно прав.')     
    
    elif message.text == 'Предложенные идеи':
        if db_admcheck(user_id, cur, con) == True:
            markup = idea_key()
            if db_takeidea(1, cur, con) == False:
                bot.send_message(user_id, 'Предложенных идей нет.')
            else:
                tg_name, photo_id, text, primary_id = db_takeidea(1, cur, con)
                sms = sms_pred(tg_name, photo_id, text)
                if photo_id == 'None':
                    bot.send_message(message.chat.id, sms, reply_markup=markup)
                else:
                    bot.send_photo(message.chat.id, open(f"mems/{photo_id}.png", 'rb'), sms, reply_markup=markup)
        else:
            bot.send_message(user_id, 'У тебя недостаточно прав.')
            
    elif message.text == 'Предложенные мемы':
        if db_admcheck(user_id, cur, con) == True:
            markup = mem_key()
            if db_takeidea(2, cur, con) == False:
                bot.send_message(user_id, 'Предложенных мемов нет.')
            else:
                tg_name, photo_id, text, primary_id = db_takeidea(2, cur, con)
                sms = sms_pred(tg_name, photo_id, text)
                if photo_id == 'None':
                    bot.send_message(message.chat.id, sms, reply_markup=markup)
                else:
                    bot.send_photo(message.chat.id, open(f"mems/{photo_id}.png", 'rb'), sms, reply_markup=markup)
        else:
            bot.send_message(user_id, 'У тебя недостаточно прав.')    
     
           
    elif message.text == 'Назад':
        markup = start_key()
        bot.send_message(message.chat.id, 'Есть сэр так точно', reply_markup=markup)
        
    elif message.text == prikol:
        if db_bancheck(user_id, cur, con) == True:
            bot.send_message(message.chat.id, 'Ты в бане черт.')
        else:
            db_tgprikol(user_id, cur, con)
            bot.send_message(user_id, 'Напиши свою идею для прикола и приложи к ней картинки (если надо). \nСделай это одним сообщением.')
            
    elif message.text == mem:
        if db_bancheck(user_id, cur, con) == True:
            bot.send_message(message.chat.id, 'Ты в бане черт.')
        else:
            db_tgmem(user_id, cur, con)
            bot.send_message(user_id, 'Скинь свой мем и подпиши его (если надо). \nСделай это одним сообщением.')
            
    else:
        if last_com(user_id, cur, con) == 1:
            if db_inccheck(user_id, cur, con) == False:
                bot.send_message(user_id, 'Твой лимит предложений на сегодня исчерпан.')
            else:
                primary_id = randint(0, 999999)
                db_tgideamem(user_id, str(message.from_user.username), 'None', message.text, primary_id, cur, con, 1)
                bot.send_message(user_id, 'Записал твою идею.')
        elif last_com(user_id, cur, con) == 2:
            bot.send_message(user_id, 'Чувак, мем это картинка, а не текст.')
        else:
            bot.send_message(user_id, 'Не понимаю тебя.')
        db_nothing(user_id, cur, con)
 
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    con = sqlite3.connect("tg.db")
    cur = con.cursor()
    if last_com(user_id, cur, con) == 0:
        bot.send_message(user_id, 'Не понимаю тебя.')    
    elif last_com(user_id, cur, con) == 1 or last_com(user_id, cur, con) == 2:
        if db_inccheck(user_id, cur, con) == False:
            bot.send_message(user_id, 'Твой лимит предложений на сегодня исчерпан.')
        else:
            photo = message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            photo_id = randint(0, 999999)
            photo_name = str(photo_id) + '.png'
            save_path = photo_name
            with open('mems/' + save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
        if last_com(user_id, cur, con) == 1:
            db_tgideamem(user_id, str(message.from_user.username), photo_id, message.caption, photo_id, cur, con, 1)
            bot.send_message(user_id, 'Я записал...')
        elif last_com(user_id, cur, con) == 2:
            db_tgideamem(user_id, str(message.from_user.username), photo_id, message.caption, photo_id, cur, con, 2)
            bot.send_message(user_id, 'Я сохранил...')
    db_nothing(user_id, cur, con)

bot.infinity_polling(none_stop=True,interval=0)