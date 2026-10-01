import socket
import threading

from ghostnet.protocol import (
    TYPE_ERROR,
    TYPE_MESSAGE,
    TYPE_REGISTER,
    ProtocolError,
    decode_packet,
    encode_packet,
)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9000


def receive_messages(client_socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(4096)

            packet = decode_packet(data)

            if packet["type"] == TYPE_MESSAGE:
                source = packet["source"]
                payload = packet["payload"]

                print(
                    f"\n{source}: {payload}"
                )
                print(
                    "> ",
                    end="",
                    flush=True,
                )

            elif packet["type"] == TYPE_ERROR:
                print(
                    f"\nServer error: "
                    f"{packet['payload']}"
                )
                print(
                    "> ",
                    end="",
                    flush=True,
                )

        except ProtocolError as exc:
            print(
                f"\nInvalid packet received: {exc}"
            )

        except OSError:
            break


def main():
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    client_name = input(
        "Choose a GhostNet name: "
    ).strip()

    registration_packet = encode_packet(
        packet_type=TYPE_REGISTER,
        source=client_name,
    )

    client_socket.sendto(
        registration_packet,
        (
            SERVER_HOST,
            SERVER_PORT,
        ),
    )

    print(
        f"Registered as '{client_name}'"
    )

    print()
    print(
        "Send messages using:"
    )
    print(
        "destination:message"
    )
    print()
    print(
        "Example:"
    )
    print(
        "client2:hello"
    )
    print()
    print(
        "Type 'exit' to quit.\n"
    )

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
            print(
                "Use format: "
                "destination:message"
            )
            continue

        destination, message = (
            user_input.split(":", 1)
        )

        packet = encode_packet(
            packet_type=TYPE_MESSAGE,
            source=client_name,
            destination=destination,
            payload=message,
        )

        client_socket.sendto(
            packet,
            (
                SERVER_HOST,
                SERVER_PORT,
            ),
        )

    client_socket.close()


if __name__ == "__main__":
    main()