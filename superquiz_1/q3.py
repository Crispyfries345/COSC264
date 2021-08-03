def destaddress(pkt: bytearray) -> "tuple[int, str]":
    packet_h: int = int.from_bytes(pkt[:20], "big")
    dest_addr: int = packet_h & 0xFFFFFFFF
    dest_str: str = f"{dest_addr >> 24}.{(dest_addr >> 16) & 0xFF}.{(dest_addr >> 8) & 0xFF}.{dest_addr & 0xFF}"
    return dest_addr, dest_str


print(
    destaddress(bytearray(b"E\x00\x00\x1e\x04\xd2\x00\x00@\x06\x00\x00\x00\x124V3DUf"))
)
