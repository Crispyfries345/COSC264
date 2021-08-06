from argparse import ArgumentParser
from io import TextIOWrapper
import socket
from shared import (
    valid_port,
    sock_recv,
    MAGIC_NO,
    SOCKET_TIMEOUT,
)
import datetime as dt
import os
import sys

# max FileRequest in bytes. Next-largest power of two from the 1029 max request size
MAX_FILE_REQUEST: int = 2048
FILE_REQUEST_TYPE: int = 1


def parse_file_request(file_request: bytes) -> str:
    """Parses the FileRequest and returns the requested filename"""
    magic_no: int = (file_request[0] << 8) | file_request[1]
    fr_type: int = file_request[2]
    filename_len_h: int = (file_request[3] << 8) | file_request[4]

    if magic_no != MAGIC_NO:
        raise ValueError(
            f"The received magic number ({magic_no:#x}) does not match {MAGIC_NO:#x}"
        )
    if fr_type != FILE_REQUEST_TYPE:
        raise ValueError(
            f"The type of the file transaction ({fr_type}) is not a file request ({FILE_REQUEST_TYPE})"
        )
    if not 1 <= filename_len_h <= 1024:
        raise ValueError(
            f"The length of the filename ({filename_len_h}) must be between 1 and 1024"  # TODO const
        )

    filename: bytes = file_request[5:]
    filename_len: int = len(filename)
    if filename_len != filename_len_h:
        raise ValueError(
            f"The length of the filename ({filename_len}) does not match the length specified in the header ({filename_len_h})"
        )
    return filename.decode("utf-8")


def create_file_response(filename: str) -> bytearray:
    """Creates a FileResponse byte array"""
    file_response: bytearray = bytearray()
    file_response.append(MAGIC_NO >> 8)
    file_response.append(MAGIC_NO & 0xFF)
    file_response.append(2)

    try:
        filepath: str = os.path.join(
            os.path.dirname(__file__), "server_files", filename
        )
        file: TextIOWrapper
        with open(filepath, "rb") as file:
            file_response.append(1)
            file_bytes: bytes = file.read()
            data_length: int = len(file_bytes)
            file_response.append(data_length >> 24)
            file_response.append((data_length >> 16) & 0xFF)
            file_response.append((data_length >> 8) & 0xFF)
            file_response.append(data_length & 0xFF)
            file_response += file_bytes
    except FileNotFoundError:
        for _ in range(5):
            file_response.append(0)

    return file_response


def main():
    """Main function"""
    parser = ArgumentParser(description="File transfer server")
    parser.add_argument("port", type=valid_port, help="server port")
    args = parser.parse_args()

    try:
        sockfd: socket.socket = socket.socket()
    except OSError as err:
        sys.exit(err)

    try:
        sockfd.bind(("", args.port))
        sockfd.listen()
    except OSError as err:
        sockfd.close()
        sys.exit(err)

    while True:
        conn: socket.socket
        addr: tuple[str, int]
        conn, addr = sockfd.accept()
        with conn:
            conn.settimeout(SOCKET_TIMEOUT)
            print(f"{dt.datetime.utcnow()} - {addr[0]}:{addr[1]}")
            data: bytes = sock_recv(conn, MAX_FILE_REQUEST)
            filename: str = parse_file_request(data)
            file_response: bytearray = create_file_response(filename)
            conn.send(file_response)
            conn.close()
            print(f"{len(file_response)}")


if __name__ == "__main__":
    main()
