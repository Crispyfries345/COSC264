from argparse import ArgumentTypeError
import socket
import sys

PORT_MIN: int = 1024
PORT_MAX: int = 64_000
MAGIC_NO: int = 0x497E
SOCKET_TIMEOUT: int = 1
FILE_RESPONSE_HEADER_S: int = 8  # size in bytes


def valid_port(port: str) -> int:
    """Validates a given port number"""
    port_int: int = int(port)
    if not PORT_MIN <= port_int <= PORT_MAX:
        raise ArgumentTypeError(f"{port} is not a valid port number")
    return port_int


def sock_recv(conn: socket.socket, response_len: int) -> bytes:
    try:
        file_response: bytes = conn.recv(response_len)
    except socket.timeout as err:
        conn.close()
        sys.exit(err)
    return file_response
