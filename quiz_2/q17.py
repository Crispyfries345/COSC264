from numbers import Number


def transmission_delay(packetLength_bytes: Number, rate_mbps: Number) -> Number:
    return (packetLength_bytes * 8) / (rate_mbps)


print("{:.3f}".format(transmission_delay(1000000, 4000000)))
