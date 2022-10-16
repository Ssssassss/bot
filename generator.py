from random import randint

def generator_number(staples:bool = True)->(str, int):
    signs = ('+', '-', '()') if staples else ('+', '-')
    ans_number = randint(-50, 100)
    ans_str = str(ans_number)

    for i in range(randint(2, 4)):
        rand_number = randint(-50, 100)
        str_number = str(rand_number)
        sign = randint(0, len(signs) - 1)
        if ( sign == 2 ) :
            ans = generator_number(False)
            rand_number = ans[1]
            sign = randint(0, len(signs) - 2)
            str_number = '(' + ans[0] + ')'
        
        if ( sign == 0 ):
            ans_number += rand_number
        else :
            ans_number -= rand_number

        ans_str +=  signs[sign] + str_number
    ans_str = '+'.join(ans_str.split('--'))
    ans_str = '-'.join(ans_str.split('-+'))
    ans_str = '-'.join(ans_str.split('+-'))
    
    return ans_str, ans_number


def generator(size:int)->list:
     return [ generator_number() for i in range(size)]
