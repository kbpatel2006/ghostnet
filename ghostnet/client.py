import socket


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9000


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("ghostnet client")
    print("Type a message and press Enter.")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("> ")

        if message.lower() == "exit":
            break

        client_socket.sendto(
            message.encode("utf-8"),
            (SERVER_HOST, SERVER_PORT),
        )

    client_socket.close()


if __name__ == "__main__":
    main()