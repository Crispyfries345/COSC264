def message_delay(
    connSetupTime_s, cableLength_km, speedOfLight_kms, messageLength_b, dataRate_bps
):
    delay: float = connSetupTime_s
    delay += (cableLength_km / speedOfLight_kms) * 2
    delay += messageLength_b / dataRate_bps
    return delay


print("{:.3f}".format(message_delay(0.2, 10_000, 200_000, 1_000_000_000, 1_000_000)))
