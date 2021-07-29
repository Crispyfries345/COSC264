from argparse import ArgumentParser, ArgumentTypeError
import socket
import sys

PORT_MIN: int = 1024
PORT_MAX: int = 64_000
SOCKADDR_I: int = 4  # index of sockaddr returned by getaddrinfo


def get_ipv4_addr(addr: str, port: int) -> str:
    """Gets an IPv4 address for a given address and port,
    performing a DNS lookup if address is a hostname"""
    try:
        ipv4_addr: str = socket.getaddrinfo(
            addr, port, family=socket.AF_INET, type=socket.SOCK_STREAM
        )[0][SOCKADDR_I][0]
    except socket.gaierror as exc:
        print(exc)
        sys.exit(1)
    return ipv4_addr


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
    port: int = args.port
    ipv4_addr: str = get_ipv4_addr(args.address, port)
    sockfd: socket.socket = socket.socket()
    sockfd.connect((ipv4_addr, port))   


if __name__ == "__main__":
    main()
