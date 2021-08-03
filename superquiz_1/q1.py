def composepacket(
    version: int,
    hdrlen: int,
    tosdscp: int,
    totallength: int,
    identification: int,
    flags: int,
    fragmentoffset: int,
    timetolive: int,
    protocoltype: int,
    headerchecksum: int,
    sourceaddress: int,
    destinationaddress: int,
):
    if version != 4:
        return 1
    if hdrlen.bit_length() > 4 or hdrlen < 0:
        return 2
    if tosdscp.bit_length() > 6 or tosdscp < 0:
        return 3
    if totallength.bit_length() > 16 or totallength < 0:
        return 4
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
    if headerchecksum.bit_length() > 16 or headerchecksum < 0:
        return 10
    if sourceaddress.bit_length() > 32 or sourceaddress < 0:
        return 11
    if destinationaddress.bit_length() > 32 or destinationaddress < 0:
        return 12
    packet: int = destinationaddress
    packet |= sourceaddress << 32
    packet |= headerchecksum << 64
    packet |= protocoltype << 80
    packet |= timetolive << 88
    packet |= fragmentoffset << 96
    packet |= identification << 112
    packet |= totallength << 128
    packet |= tosdscp << 144
    packet |= hdrlen << 152
    packet |= version << 156

    return bytearray(packet.to_bytes(20, "big"))


print(composepacket(4, 5, 0, 1500, 24200, 0, 63, 22, 6, 4711, 2190815565, 3232270145))
