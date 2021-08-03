def basicpacketcheck(pkt: bytearray):
    packet_len: int = len(pkt)
    if packet_len < 20:
        return 1
    packet_h: int = int.from_bytes(pkt[:20], "big")
    version: int = packet_h >> 156
    if version != 4:
        return 2

    sum_x: int = (
        (packet_h >> 144)
        + ((packet_h >> 128) & 0xFFFF)
        + ((packet_h >> 112) & 0xFFFF)
        + ((packet_h >> 96) & 0xFFFF)
        + ((packet_h >> 80) & 0xFFFF)
        + ((packet_h >> 64) & 0xFFFF)
        + ((packet_h >> 48) & 0xFFFF)
        + ((packet_h >> 32) & 0xFFFF)
        + ((packet_h >> 16) & 0xFFFF)
        + (packet_h & 0xFFFF)
    )
    while sum_x.bit_length() > 16:
        sum_x0: int = sum_x & 0xFFFF
        sum_x1: int = sum_x >> 16
        sum_x = sum_x0 + sum_x1
    if sum_x != 0xFFFF:
        return 3

    total_len: int = (packet_h >> 128) & 0xFFFF
    if packet_len != total_len:
        return 4

    return True


print(
    basicpacketcheck(
        bytearray(
            [
                0x45,
                0x0,
                0x0,
                0x1E,
                0x4,
                0xD2,
                0x0,
                0x0,
                0x40,
                0x6,
                0x20,
                0xB4,
                0x12,
                0x34,
                0x56,
                0x78,
                0x98,
                0x76,
                0x54,
                0x32,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
                0x0,
            ]
        )
    )
)
