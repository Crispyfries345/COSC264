def encodedate(day, month, year):
    if (1 <= day <= 31) and (1 < month <= 12) and (0 <= year <= 2 ** 23):
        date: int = 0
        date |= (month - 1) << 28
        date |= (day - 1) << 23
        date |= year
        return date
    return -1


print(encodedate(5, 5, 2017))
