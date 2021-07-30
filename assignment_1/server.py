from argparse import ArgumentParser
import socket
from shared import valid_port, byte_len, MAGIC_NO
import datetime as dt

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


def main():
    parser = ArgumentParser(description="...")
    parser.add_argument("port", type=valid_port, help="server port")
    args = parser.parse_args()

    sockfd: socket.socket = socket.socket()
    sockfd.bind(("", args.port))
    sockfd.listen()
    while True:
        conn: socket.socket
        addr: tuple[str, int]
        conn, addr = sockfd.accept()
        print(f"{dt.datetime.utcnow()} - {addr[0]}:{addr[1]}")
        data: bytes = conn.recv(MAX_FILE_REQUEST)
        filename: str = parse_file_request(data)
        pass


if __name__ == "__main__":
    main()
