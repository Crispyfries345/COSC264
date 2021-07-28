def avg_trials_from_ber(bit_error_probability, packetLength_b):
    return 1 / (1 - per_from_ber(bit_error_probability, packetLength_b))


def per_from_ber(bitErrorProb, packetLen_b):
    return 1 - (1 - bitErrorProb) ** packetLen_b


print("{:.3f}".format(avg_trials_from_ber(0.001, 2000)))
