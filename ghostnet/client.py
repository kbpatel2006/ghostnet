import socket
import threading
import time

from ghostnet.protocol import (
    TYPE_DISCONNECT,
    TYPE_ERROR,
    TYPE_HEARTBEAT,
    TYPE_MESSAGE,
    TYPE_REGISTER,
    ProtocolError,
    decode_packet,
    encode_packet,
)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9000

HEARTBEAT_INTERVAL = 5


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


def send_heartbeats(
    client_socket,
    client_name,
    stop_event,
):
    while not stop_event.wait(
        HEARTBEAT_INTERVAL
    ):
        packet = encode_packet(
            packet_type=TYPE_HEARTBEAT,
            source=client_name,
        )

        try:
            client_socket.sendto(
                packet,
                (
                    SERVER_HOST,
                    SERVER_PORT,
                ),
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

    if not client_name:
        print("Client name cannot be empty.")
        return

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
    print("Send messages using:")
    print("destination:message")
    print()
    print("Type 'exit' to quit.\n")

    stop_event = threading.Event()

    receiver_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True,
    )

    heartbeat_thread = threading.Thread(
        target=send_heartbeats,
        args=(
            client_socket,
            client_name,
            stop_event,
        ),
        daemon=True,
    )

    receiver_thread.start()
    heartbeat_thread.start()

    try:
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

            destination = destination.strip()

            if not destination:
                print(
                    "Destination cannot be empty."
                )
                continue

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

    except KeyboardInterrupt:
        print("\nDisconnecting...")

    finally:
        stop_event.set()

        disconnect_packet = encode_packet(
            packet_type=TYPE_DISCONNECT,
            source=client_name,
        )

        try:
            client_socket.sendto(
                disconnect_packet,
                (
                    SERVER_HOST,
                    SERVER_PORT,
                ),
            )

        except OSError:
            pass

        client_socket.close()


if __name__ == "__main__":
    main()