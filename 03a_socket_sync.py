from socket import create_connection


def fetch(size: int):
    con = create_connection(("coherentminds.de", 32154))

    con.sendall(f"{size}\n".encode())

    data = b""
    while len(data) < size:
        data += con.recv(size - len(data))

    con.close()
    print(f"received {len(data)} bytes")


def main():
    for _ in range(10):
        fetch(32 * 1024)


if __name__ == "__main__":
    main()
