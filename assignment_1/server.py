from argparse import ArgumentParser
from io import TextIOWrapper
import socket
from shared import valid_port, byte_len, MAGIC_NO, SOCKET_TIMEOUT
import datetime as dt
import os
import sys

# max FileRequest in bytes. Next-largest power of two from the 1029 max request size
MAX_FILE_REQUEST: int = 2048


def parse_file_request(file_request: bytes) -> str:
    """Parses the FileRequest and returns the requested filename"""
    fr_int: int = int.from_bytes(file_request, "big")
    if not fr_int & 0xFFFF == MAGIC_NO:
        pass
    if not (fr_int >> 16) & 0xFF == 1:
        pass
    filename_len: int = (fr_int >> 24) & 0xFFFF
    if not 1 <= filename_len <= 1024:
        pass
    filename_raw: int = fr_int >> 40
    filename: bytes = filename_raw.to_bytes(byte_len(filename_raw), "big")
    if len(filename) != filename_len:
        pass
    return filename.decode("utf-8")


def create_file_response(filename: str) -> bytes:
    """Creates a FileResponse"""
    file_response: int = MAGIC_NO
    file_response |= 2 << 16

    try:
        file: TextIOWrapper = open(
            os.path.join(os.path.dirname(__file__), "server_files", filename), "rb"
        )
        file_response |= 1 << 24
    except FileNotFoundError:
        pass

    file_bytes: bytes = file.read()
    file_response |= len(file_bytes) << 32
    file_response |= int.from_bytes(file_bytes, "big") << 64

    file.close()
    return file_response.to_bytes(byte_len(file_response), "big")


def main():
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
            data: bytes = conn.recv(MAX_FILE_REQUEST)
            filename: str = parse_file_request(data)
            file_response: bytes = create_file_response(filename)
            conn.send(file_response)
            conn.close()
            print(f"{len(file_response)}")


if __name__ == "__main__":
    main()
