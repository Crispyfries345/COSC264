from argparse import ArgumentParser, Namespace
import io
from shared import (
    FILE_RESPONSE_TYPE,
    valid_port,
    sock_recv,
    MAGIC_NO,
    SOCKET_TIMEOUT,
    FILE_RESPONSE_HEADER_S,
    FILE_RESPONSE_TYPE,
    VALID_STATUS_CODE,
)
import socket
import sys
import os


SOCKADDR_I: int = 4  # index of sockaddr returned by getaddrinfo
MAX_FILE_RESPONSE: int = 4096


def validate_resp_h(file_response: bytes) -> int:
    """Validates the FileResponse header, returning the length of the file data"""
    packet_len: int = len(file_response)
    if packet_len < FILE_RESPONSE_HEADER_S:
        raise ValueError(
            f"The size of the received packet ({packet_len}B) is too small to be a FileResponse"
        )
    magic_no: int = (file_response[0] << 8) | file_response[1]
    fr_type: int = file_response[2]
    status_code: int = file_response[3]
    data_len: int = (
        (file_response[4] << 24)
        | (file_response[5] << 16)
        | (file_response[6] << 8)
        | file_response[7]
    )

    if magic_no != MAGIC_NO:
        raise ValueError(
            f"The received magic number ({magic_no:#x}) does not match {MAGIC_NO:#x}"
        )
    if fr_type != FILE_RESPONSE_TYPE:
        raise ValueError(
            f"The type of the file transaction ({fr_type}) is not a file response ({FILE_RESPONSE_TYPE})"
        )
    if status_code != VALID_STATUS_CODE:
        raise ValueError(f"File does not exist on server")

    return data_len


def store_file_response(conn: socket.socket, filename: str) -> int:
    """Parses a file response, returning the size of the received data"""
    file_response: bytes = sock_recv(conn, MAX_FILE_RESPONSE)
    data_len: int = validate_resp_h(file_response)
    try:
        os.mkdir(os.path.join(os.path.dirname(__file__), "client_files"))
    except FileExistsError:
        pass
    file: io.BufferedWriter = open(
        os.path.join(os.path.dirname(__file__), "client_files", filename), "wb"
    )
    tmp_f: io.BytesIO = io.BytesIO()
    file_size: int = len(file_response) - FILE_RESPONSE_HEADER_S
    tmp_f.write(file_response[8:])
    file_response = sock_recv(conn, MAX_FILE_RESPONSE)
    while file_response:
        file_size += len(file_response)
        tmp_f.write(file_response)
        file_response = sock_recv(conn, MAX_FILE_RESPONSE)

    if file_size != data_len:
        raise ValueError(
            f"The file size specified in the header ({data_len}) differs from the actual data size ({file_size})"
        )

    file.write(tmp_f.getbuffer())
    file.close()
    return data_len


def create_file_request(filename: str) -> bytearray:
    """Creates a FileRequest byte array"""
    file_request: bytearray = bytearray()
    file_request.append(MAGIC_NO >> 8)
    file_request.append(MAGIC_NO & 0xFF)
    file_request.append(1)
    encoded_filename: bytes = filename.encode("utf-8")
    filename_len: int = len(filename)
    file_request.append(filename_len >> 8)
    file_request.append(filename_len & 0xFF)
    return file_request + encoded_filename


def get_ipv4_addr(addr: str, port: int) -> str:
    """Gets an IPv4 address for a given address and port,
    performing a DNS lookup if address is a hostname"""
    ipv4_addr: str = socket.getaddrinfo(
        addr, port, family=socket.AF_INET, type=socket.SOCK_STREAM
    )[0][SOCKADDR_I][0]
    return ipv4_addr


def parse_args() -> Namespace:
    """Parses the relevant arguments"""
    parser = ArgumentParser(description="File-transfer client")
    parser.add_argument("address", help="ip address or hostname of server")
    parser.add_argument("port", type=valid_port, help="server port")
    parser.add_argument("filename", help="name of file to be retrieved from server")
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_args()
    port: int = args.port
    filename: str = args.filename
    if os.path.isfile(
        os.path.join(os.path.dirname(__file__), "client_files", filename)
    ):
        sys.exit(f"{filename} already exists in client_files")
    try:
        ipv4_addr: str = get_ipv4_addr(args.address, port)
        sockfd: socket.socket = socket.socket()
    except OSError as err:
        sys.exit(err)
    sockfd.settimeout(SOCKET_TIMEOUT)
    try:
        sockfd.connect((ipv4_addr, port))
    except Exception as err:
        sys.exit(err)
    file_request: bytearray = create_file_request(filename)
    sockfd.send(file_request)
    try:
        data_len: int = store_file_response(sockfd, filename)
    except Exception as err:
        sys.exit(err)
    print(f'Received the file "{filename}" of size {data_len} bytes')


if __name__ == "__main__":
    main()
