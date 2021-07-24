def decodedate (x):
    month: int = (x >> 28) + 1
    day: int = ((x & 0xF800000) >> 23) + 1
    year: int = (x & 0x7FFFFF)
    return f"{day}.{month}.{year}"

print(decodedate(1107298273))