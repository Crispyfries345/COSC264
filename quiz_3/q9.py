def total_transfer_time(
    linkLength_km,
    speedOfLight_kms,
    processingDelay_s,
    dataRate_bps,
    maxUserDataBitsPerPacket_b,
    overheadBitsPerPacket_b,
    messageLength_b,
):
    l = linkLength_km
    c = speedOfLight_kms
    p = processingDelay_s
    r = dataRate_bps
    s = maxUserDataBitsPerPacket_b
    o = overheadBitsPerPacket_b
    m = messageLength_b
    total_length = (m / s) * o + m
    trans_time: float = 2 * (l / c)
    trans_time += 2 * p + (s + o) / r
    trans_time += total_length / r
    return trans_time


print(
    "{:.5f}".format(
        total_transfer_time(
            10_000, 200_000, 0.001, 1_000_000, 1_000, 100, 1_000_000_000
        )
    )
)
