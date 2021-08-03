from argparse import ArgumentParser
from io import TextIOWrapper
import socket
from shared import (
    valid_port,
    byte_len,
    sock_recv,
    MAGIC_NO,
    SOCKET_TIMEOUT,
    FILE_RESPONSE_HEADER_S,
)
import datetime as dt
import os
import sys

# max FileRequest in bytes. Next-largest power of two from the 1029 max request size
MAX_FILE_REQUEST: int = 2048
FILE_REQUEST_TYPE: int = 1


def parse_file_request(file_request: bytes) -> str:
    """Parses the FileRequest and returns the requested filename"""
    fr_int: int = int.from_bytes(file_request, "big")
    magic_no: int = fr_int & 0xFFFF
    fr_type: int = (fr_int >> 16) & 0xFF
    filename_len_h: int = (fr_int >> 24) & 0xFFFF

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

    filename_raw: int = fr_int >> 40
    filename: bytes = filename_raw.to_bytes(byte_len(filename_raw), "big")
    filename_len: int = len(filename)
    if filename_len != filename_len_h:
        raise ValueError(
            f"The length of the filename ({filename_len}) does not match the length specified in the header ({filename_len_h})"
        )
    return filename.decode("utf-8")


def create_file_response(filename: str) -> bytes:
    """Creates a FileResponse byte array"""
    file_response: int = MAGIC_NO
    file_response |= 2 << 16  # TODO lsb first!

    try:
        filepath: str = os.path.join(
            os.path.dirname(__file__), "server_files", filename
        )
        file: TextIOWrapper
        with open(filepath, "rb") as file:
            file_response |= 1 << 24
            file_bytes: bytes = file.read()
            file_response |= len(file_bytes) << 32
            file_response |= int.from_bytes(file_bytes, "big") << 64
    except FileNotFoundError:
        pass  # The rest of the bytes would remain 0

    fr_byte_len: int = byte_len(file_response)
    return file_response.to_bytes(
        fr_byte_len if fr_byte_len > FILE_RESPONSE_HEADER_S else FILE_RESPONSE_HEADER_S,
        "big",
    )


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
            file_response: bytes = create_file_response(filename)
            conn.send(file_response)
            conn.close()
            print(f"{len(file_response)}")


if __name__ == "__main__":
    main()
