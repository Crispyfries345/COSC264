from argparse import ArgumentTypeError

PORT_MIN: int = 1024
PORT_MAX: int = 64_000
MAGIC_NO: int = 0x497E
SOCKET_TIMEOUT: int = 1


def valid_port(port: str) -> int:
    """Validates a given port number"""
    port_int: int = int(port)
    if not PORT_MIN <= port_int <= PORT_MAX:
        raise ArgumentTypeError(f"{port} is not a valid port number")
    return port_int


def byte_len(int_: int) -> int:
    """Number of bytes to allocate for an integer"""
    return (int_.bit_length() + 7) // 8
