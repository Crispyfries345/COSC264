from argparse import ArgumentParser
from shared import valid_port, byte_len, MAGIC_NO
import socket
import sys


SOCKADDR_I: int = 4  # index of sockaddr returned by getaddrinfo
MAX_FILE_RESPONSE: int = 4096


def parse_file_response(file_response: bytes):
    """Parses a file response"""
    fr_int: int = int.from_bytes(file_response, "big")
    if not fr_int & 0xFFFF == MAGIC_NO:
        pass
    if not (fr_int >> 16) & 0xFF == 2:
        pass
    if not (fr_int >> 24) & 0xFF == 1:
        pass
    data_len: int = (fr_int >> 32) & 0xFFFFFFFF
    file_data: int = fr_int >> 64
    pass


def create_file_request(filename: str) -> bytes:
    file_request: int = MAGIC_NO
    file_request |= 1 << 16
    encoded_filename: bytes = filename.encode("utf-8")
    file_request |= len(encoded_filename) << 24  # TODO constrain
    file_request |= int.from_bytes(encoded_filename, "big") << 40
    return file_request.to_bytes(byte_len(file_request), "big")


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
    file_request: bytes = create_file_request(args.filename)
    sockfd.send(file_request)
    file_response: bytes = sockfd.recv(MAX_FILE_RESPONSE)
    parse_file_response(file_response)


if __name__ == "__main__":
    main()
