from argparse import ArgumentParser
from shared import valid_port
import socket
import sys


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
