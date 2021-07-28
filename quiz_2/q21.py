from numbers import Number

def queueing_delay (rate_bps: Number, numPackets: Number, packetLength_b: Number) -> Number:
    return (numPackets * packetLength_b) / rate_bps

print ("{:.3f}".format(queueing_delay(1000000, 7, 10000)))
