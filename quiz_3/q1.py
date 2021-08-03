def connection_setup_delay(
    cableLength_km, speedOfLight_kms, dataRate_bps, messageLength_b, processingTimes_s
):
    delay: float = 4 * processingTimes_s
    delay += (messageLength_b / dataRate_bps) * 4
    delay += (cableLength_km / speedOfLight_kms) * 4
    return delay


print("{:.4f}".format(connection_setup_delay(10_000, 200_000, 1_000_000, 4_000, 0.001)))
