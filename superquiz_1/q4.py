def payload(pkt: bytearray) -> bytearray:

    header_len: int = pkt[0] & 0xF
    return pkt[header_len * 4 :]


print(
    payload(
        bytearray(b'E\x00\x00\x17\x00\x00\x00\x00@\x06i\x8d\x11"3DUfw\x88\x10\x11\x12')
    )
)
