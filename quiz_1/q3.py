import math
def convert(x, base):
    if type(x) is not int:
        return -1
    if type(base) is not int:
        return -2
    if x < 0:
        return -3
    if base < 2:
        return -4
    coefs = []
    max_exp = int(math.log(x, base))
    n: int = max_exp
    remainder = x
    while n >= 0:
        
        coef = remainder//(base**n)
        coefs.append(coef)
        remainder -= coef * base ** n
        n -= 1
    return coefs