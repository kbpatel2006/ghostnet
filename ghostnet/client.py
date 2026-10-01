import socket
import threading


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9000


def receive_messages(client_socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(4096)
            message = data.decode("utf-8")

            if message.startswith("MESSAGE:"):
                payload = message.split(":", 1)[1]

                print(f"\nReceived: {payload}")
                print("> ", end="", flush=True)

            elif message.startswith("ERROR:"):
                error = message.split(":", 1)[1]

                print(f"\nServer error: {error}")
                print("> ", end="", flush=True)

        except OSError:
            break


def main():
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    client_name = input("Choose a ghostnet name: ").strip()

    registration_message = f"REGISTER:{client_name}"

    client_socket.sendto(
        registration_message.encode("utf-8"),
        (SERVER_HOST, SERVER_PORT),
    )

    print(f"Registered as '{client_name}'")
    print()
    print("Send messages using:")
    print("destination:message")
    print()
    print("Example:")
    print("client2:hello")
    print()
    print("Type 'exit' to quit.\n")

    receiver_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True,
    )

    receiver_thread.start()

    while True:
        user_input = input("> ")

        if user_input.lower() == "exit":
            break

        if ":" not in user_input:
            print("Use format: destination:message")
            continue

        destination, message = user_input.split(":", 1)

        packet = f"SEND:{destination}:{message}"

        client_socket.sendto(
            packet.encode("utf-8"),
            (SERVER_HOST, SERVER_PORT),
        )

    client_socket.close()


if __name__ == "__main__":
    main()