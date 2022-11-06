from generator import generator
from tegs_ans import tegs
from telebot import *
from time import *
from parser import *
import sys

def main(argc:int, argv:list)->int:
    TOKEN = None
    if ( argc > 2 ) :
        print("Error: the supplied argument must be current one or not at all!")
        return 1

    if ( argc == 1 ) :
        TOKEN = input("Enter the bot token: ").strip()
    
    else :
        TOKEN = argv[-1]

    bot = TeleBot(TOKEN)
    token = {}

    @bot.message_handler(content_types=["text"])
    def massage(message)->None:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("3 задачи")
        btn2 = types.KeyboardButton("6 задач")
        btn3 = types.KeyboardButton("9 задач")
        markup.add(btn1, btn2).row(btn3)
        
        print("Classic mode: ", asctime(localtime(time())), 
                                message.from_user.first_name, 
                                message.from_user.id)
        
        if ( len(message.text) > 1860 ) :
            bot.send_message(message.from_user.id, "Текст слишком большой", reply_markup = markup)
            return None

        elif ( message.text in tegs) :
            bot.send_message(message.from_user.id, tegs[message.text], parse_mode = "html", reply_markup = markup)
            return None

        elif ( message.text == "3 задачи" and not (message.from_user.id in token) ) :
            j = 1
            str_ans = ""
            other = []
            for i in generator(3):
                str_ans += str(j) + ".  " +  i[0] + "\n"
                other.append(i[1])
                j += 1
                
            bot.send_message(message.from_user.id, str_ans)
            token[message.from_user.id] = other, time()
            return None

        elif ( message.text == "6 задач" and not (message.from_user.id in token) ) :
            j = 1
            str_ans = ""
            other = []
            for i in generator(6):
                str_ans += str(j) + ".  " +  i[0] + "\n"
                other.append(i[1])
                j += 1
                
            bot.send_message(message.from_user.id, str_ans)
            token[message.from_user.id] = other, time()
            return None

        elif ( message.text == "9 задач" and not (message.from_user.id in token) ) :
            j = 1
            str_ans = ""
            other = []
            for i in generator(9):
                str_ans += str(j) + ".  " +  i[0] + "\n"
                other.append(i[1])
                j += 1
                
            bot.send_message(message.from_user.id, str_ans)
            token[message.from_user.id] = other, time()
            return None


        
        else:
            if ( not (message.from_user.id in token) ) :
                ans = "Я не понимаю что ты хочешь!! Выбери из меню что ты хочешь!!"
                bot.send_message(message.from_user.id, ans, reply_markup = markup)
                return None
            other = ans_test(message.text, len(token[message.from_user.id]) + 1)
            if ( other == None ) :
                ans = """Я не понимаю что ты хочешь!! Если ты хочешь
                новую задачу то реши сначало страую"""
                bot.send_message(message.from_user.id, ans)
                return None

            x = 0
            for i in range(len(token[message.from_user.id][0])):
             
                if ( other[i] == token[message.from_user.id][0][i] ):
                    x += 1
            k = int(time() - token[message.from_user.id][1]) 
            seconds = k % 60
            k //= 60
            minutes = k % 60
            k //= 60
            hours = k % 60
            timeAns = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        
            ans = "Вы решили " + str(x) + "/" + str(len(token[message.from_user.id][0]))
            ans += " задач решено верно. Твое время: " + timeAns + ". Попробуй снова для лучшего результата!!"
            del token[message.from_user.id]
            bot.send_message(message.from_user.id, ans, reply_markup = markup)



        



    bot.polling(none_stop = True, timeout = 120)


if ( __name__ == "__main__" ) :
    exit(main(len(sys.argv), sys.argv))
