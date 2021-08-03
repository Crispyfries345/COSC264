def revisedcompose(
    hdrlen,
    tosdscp,
    identification,
    flags,
    fragmentoffset,
    timetolive,
    protocoltype,
    sourceaddress,
    destinationaddress,
    payload,
):
    if hdrlen.bit_length() > 4 or hdrlen < 5:
        return 2
    if tosdscp.bit_length() > 6 or tosdscp < 0:
        return 3

    if identification.bit_length() > 16 or identification < 0:
        return 5

    if flags.bit_length() > 3 or flags < 0:
        return 6
    if fragmentoffset.bit_length() > 13 or fragmentoffset < 0:
        return 7
    if timetolive.bit_length() > 8 or timetolive < 0:
        return 8
    if protocoltype.bit_length() > 8 or protocoltype < 0:
        return 9
    # if headerchecksum.bit_length() > 16 or headerchecksum < 0:
    #     return 10
    if sourceaddress.bit_length() > 32 or sourceaddress < 0:
        return 11
    if destinationaddress.bit_length() > 32 or destinationaddress < 0:
        return 12
    packet: bytearray = bytearray()
    packet.append(4 << 4 | hdrlen)
    packet.append(tosdscp << 2)
    total_len: int = len(payload) + hdrlen * 4
    packet.append(total_len >> 8)
    packet.append(total_len & 0xFF)
    packet.append(identification >> 8)
    packet.append(identification & 0xFF)
    packet.append(flags << 5 | fragmentoffset >> 7)
    packet.append(fragmentoffset & 0xFF)
    packet.append(timetolive)
    packet.append(protocoltype)
    packet.append(0)
    packet.append(0)
    packet.append(sourceaddress >> 24)
    packet.append((sourceaddress >> 16) & 0xFF)
    packet.append((sourceaddress >> 8) & 0xFF)
    packet.append(sourceaddress & 0xFF)
    packet.append(destinationaddress >> 24)
    packet.append((destinationaddress >> 16) & 0xFF)
    packet.append((destinationaddress >> 8) & 0xFF)
    packet.append(destinationaddress & 0xFF)
    for _ in range(hdrlen - 5):
        for _ in range(4):
            packet.append(0)

    sum_x: int = 0
    for i in range(0, hdrlen * 4, 2):
        sum_x += packet[i] << 8 | packet[i + 1]
    while sum_x.bit_length() > 16:
        sum_x0: int = sum_x & 0xFFFF
        sum_x1: int = sum_x >> 16
        sum_x = sum_x0 + sum_x1
    sum_x = ~sum_x & 0xFFFF
    packet[10] = sum_x >> 8
    packet[11] = sum_x & 0xFF
    return packet + payload


print(
    revisedcompose(
        6,
        24,
        4711,
        0,
        22,
        64,
        0x06,
        0x22334455,
        0x66778899,
        bytearray([0x10, 0x11, 0x12, 0x13, 0x14, 0x15]),
    )
)
