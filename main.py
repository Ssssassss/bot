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
        print("Classic mode: ", asctime(localtime(time())), 
                                message.from_user.first_name, 
                                message.from_user.id)
        
        if ( len(message.text) > 1860 ) :
            bot.send_message(message.from_user.id, "Текст слишком большой")
            return None

        elif ( message.text in tegs) :
            bot.send_message(message.from_user.id, tegs[message.text], parse_mode = "html")
            return None

        elif ( message.text[:5] == "/test" and not(message.from_user.id in token )) :         
            sizeT = size_test(message.text)
            if ( sizeT == None ) :
                ans = "Числа пиши правилнее я не могу тебя понять если забыл то <b>/help</b> в помощь"
                bot.send_message(message.from_user.id, ans,  parse_mode = "html")
                return None

            elif ( sizeT > 10 or sizeT < 0 ) :
                bot.send_message(message.from_user.id, "Сток тестов не могу сгенерить прости :)")
                return None
            
            j = 1
            str_ans = ""
            other = []
            for i in generator(sizeT):
                str_ans += str(j) + ".  " +  i[0] + "\n"
                other.append(i[1])
                j += 1
                
            bot.send_message(message.from_user.id, str_ans)
            token[message.from_user.id] = other, time()
            return None

        elif ( message.text[:5] == "/test" and message.from_user.id in token ) :     
            ans = "У важаемый у тебя еще открыт тест не забывай как ток решишь и скинешь ответ мне и я придумаю новый тест!!\
                   Завершите так сказть свой открытый гельштайль"
            bot.send_message(message.from_user.id, ans)
            return None

        else:
            if ( not (message.from_user.id in token) ) :
                ans = "Я не понимаю что ты хочешь!!"
                bot.send_message(message.from_user.id, ans)
                return None
            other = ans_test(message.text, len(token[message.from_user.id]))
            if ( other == None ) :
                ans = "Я не понимаю что ты хочешь!!"
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
            bot.send_message(message.from_user.id, ans)



        



    bot.polling(none_stop = True, timeout = 120)



main(len(sys.argv), sys.argv)

