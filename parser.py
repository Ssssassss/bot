def ans_test(other:str, len_ans_test:int)->list:
    ans = [None] * len_ans_test
    for i in other.split('\n'):
        try:
            number, other = map(int, i.split('.'))
            ans[number - 1] = int(other)
        except :
            return None

    return ans


def size_test(other:str)->int:
    try:
        return int(other[5:])
    except:
        return None
