import math


def last_fragment_size(
    messageSize_bytes, overheadPerPacket_bytes, maximumNPacketSize_bytes
):
    s = messageSize_bytes
    o = overheadPerPacket_bytes
    m = maximumNPacketSize_bytes
    return s % (m - o) + o


print(last_fragment_size(10_000, 20, 1_500))
