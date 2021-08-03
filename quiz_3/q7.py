def packet_transfer_time(
    linkLength_km,
    speedOfLight_kms,
    processingDelay_s,
    dataRate_bps,
    maxUserDataBitsPerPacket_b,
    overheadBitsPerPacket_b,
):
    L = linkLength_km
    C = speedOfLight_kms
    P = processingDelay_s
    R = dataRate_bps
    S = maxUserDataBitsPerPacket_b
    O = overheadBitsPerPacket_b
    trans_time: float = 2 * (L / C)
    trans_time += 2 * P
    trans_time += 2 * (S + O) / R

    return trans_time


print(
    "{:.5f}".format(packet_transfer_time(15_000, 250_000, 0.001, 1_000_000, 4_192, 100))
)
