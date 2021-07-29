from argparse import ArgumentParser
import socket
from shared import valid_port
import datetime as dt


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


if __name__ == "__main__":
    main()
