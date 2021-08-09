import math


def number_fragments(
    messageSize_bytes, overheadPerPacket_bytes, maximumNPacketSize_bytes
):
    s = messageSize_bytes
    o = overheadPerPacket_bytes
    m = maximumNPacketSize_bytes
    return math.ceil(s / (m - o))


print(number_fragments(10_000, 20, 1_500))
