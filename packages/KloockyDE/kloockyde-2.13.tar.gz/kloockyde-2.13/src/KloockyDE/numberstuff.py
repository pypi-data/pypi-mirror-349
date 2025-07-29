from infinity import Infinity


class Inf(Infinity, int):
    '''
    Objects of this class can be in calculations with int and act like infinity
    '''
    pass


def cap_float(number=None, decimals=None, round_last=True):
    '''
    caps number of digits after decimal point of 'number' to 'decimals'
        round_last: if True, last digit + 1 if next digit >= 5
    :param number:  float or float(number) works
    :param decimals:    int or int(decimals) works
    :param round_last:  bool
    :return:    float
    '''
    if number is None:
        number = 0.0
    if type(number) is not float:
        number = float(number)
    if decimals is None:
        decimals = 0
    if type(decimals) is not int:
        decimals = int(decimals)
    if type(round_last) is not bool:
        round_last = bool(round_last)
    if decimals < -1:
        raise ValueError('decimals < -1')
    elif decimals == -1:
        return number
    elif decimals == 0:
        return float(int(number))
    else:
        res = int(number * (10 ** decimals))
        if round_last and (int(((number * (10 ** decimals)) - res) * 10) >= 5):
            res += 1
        res = res / (10 ** decimals)
        return res


def fac(n):
    '''
    Calculates faculty of n with recursion
    :param n: int
    :return: int : faculty of n
    '''
    if n == 0:
        return 1
    elif n == 1:
        return n
    else:
        return n * fac(n - 1)
