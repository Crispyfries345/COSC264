from argparse import ArgumentTypeError
PORT_MIN: int = 1024
PORT_MAX: int = 64_000


def valid_port(port: str) -> int:
    """Validates a given port number"""
    port_int: int = int(port)
    if not PORT_MIN <= port_int <= PORT_MAX:
        raise ArgumentTypeError(f"{port} is not a valid port number")
    return port_int
