from numbers import Number


def total_time(cableLength_KM: Number, packetLength_b: Number) -> Number:
    trans_time: float = packetLength_b / (10 * 10 ** 9) * 1_000
    prop_time: float = cableLength_KM / 200_000 * 1000
    return trans_time + prop_time


print("{:.4f}".format(total_time(10000, 8000)))
