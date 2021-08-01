from argparse import ArgumentParser, Namespace
from shared import valid_port, byte_len, sock_recv, MAGIC_NO, SOCKET_TIMEOUT
import socket
import sys
import os


SOCKADDR_I: int = 4  # index of sockaddr returned by getaddrinfo
MAX_FILE_RESPONSE: int = 4096
FILE_RESPONSE_HEADER_S: int = 8  # size in bytes


def validate_resp_h(file_response: bytes) -> int:
    """Validates the FileResponse header, returning the length of the file data"""
    fr_int: int = int.from_bytes(file_response, "big")
    if not fr_int & 0xFFFF == MAGIC_NO:
        pass
    if not (fr_int >> 16) & 0xFF == 2:
        pass
    if not (fr_int >> 24) & 0xFF == 1:
        pass
    data_len: int = (fr_int >> 32) & 0xFFFFFFFF
    if not data_len:
        pass
    return data_len


def store_file_response(conn: socket.socket, filename: str) -> int:
    """Parses a file response, returning the size of the received data"""
    file_response: bytes = sock_recv(conn, MAX_FILE_RESPONSE)
    data_len: int = validate_resp_h(file_response)
    fr_int = int.from_bytes(file_response, "big")
    try:
        os.mkdir(os.path.join(os.path.dirname(__file__), "client_files"))
    except FileExistsError:
        pass
    file = open(os.path.join(os.path.dirname(__file__), "client_files", filename), "wb")
    file_size: int = len(file_response) - FILE_RESPONSE_HEADER_S
    file_data: int = fr_int >> 64
    file.write(file_data.to_bytes(byte_len(file_data), "big"))
    file_response = sock_recv(conn, MAX_FILE_RESPONSE)
    while file_response:
        file_size += len(file_response)
        file.write(file_response)
        file_response = sock_recv(conn, MAX_FILE_RESPONSE)

    if file_size != data_len:
        pass

    file.close()
    return data_len


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


def parse_args() -> Namespace:
    """Parses the relevant arguments"""
    parser = ArgumentParser(description="File-transfer client")
    parser.add_argument("address", help="ip address or hostname of server")
    parser.add_argument("port", type=valid_port, help="server port")
    parser.add_argument("filename", help="name of file to be retrieved from server")
    return parser.parse_args()


def main():

    args = parse_args()
    port: int = args.port
    filename: str = args.filename
    ipv4_addr: str = get_ipv4_addr(args.address, port)
    sockfd: socket.socket = socket.socket()
    sockfd.settimeout(SOCKET_TIMEOUT)
    sockfd.connect((ipv4_addr, port))
    file_request: bytes = create_file_request(filename)
    sockfd.send(file_request)
    data_len: int = store_file_response(sockfd, filename)
    print(f'Received the file "{filename}" of size {data_len} bytes')


if __name__ == "__main__":
    main()
