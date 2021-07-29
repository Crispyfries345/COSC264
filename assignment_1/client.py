from argparse import ArgumentParser, ArgumentTypeError
import socket

PORT_MIN: int = 1024
PORT_MAX: int = 6400


def valid_port(port: str) -> int:
    """Validates a given port number"""
    port_int: int = int(port)
    if not PORT_MIN <= port_int <= PORT_MAX:
        raise ArgumentTypeError(f"{port} is not a valid port number")
    return port_int


def main():
    parser = ArgumentParser(description="...")

    parser.add_argument("address", help="ip address or hostname of server")
    parser.add_argument("port", type=valid_port, help="server port")
    parser.add_argument("filename", help="name of file to be retrieved from server")

    args = parser.parse_args()


if __name__ == "__main__":
    main()
