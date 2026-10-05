import os
import socket
import threading

from ghostnet.protocol import (
    TYPE_DISCONNECT,
    TYPE_FRAME,
    TYPE_HEARTBEAT,
    TYPE_REGISTER,
    ProtocolError,
    decode_frame,
    decode_packet,
    encode_frame,
    encode_packet,
)
from ghostnet.tap import create_tap


SERVER_PORT = 9000
HEARTBEAT_INTERVAL = 5


def receive_packets(client_socket, tap_fd):
    while True:
        try:
            data, _ = client_socket.recvfrom(65535)
            packet = decode_packet(data)

            if packet["type"] != TYPE_FRAME:
                continue

            frame = decode_frame(
                packet["payload"]
            )

            os.write(
                tap_fd,
                frame,
            )

            print(
                f"[RECEIVED FRAME] "
                f"{len(frame)} bytes "
                f"from {packet['source']}"
            )

        except ProtocolError as exc:
            print(
                f"[INVALID PACKET] {exc}"
            )

        except OSError:
            break


def send_heartbeats(
    client_socket,
    server_address,
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
                server_address,
            )
        except OSError:
            break


def main():
    server_host = input(
        "GhostNet server address: "
    ).strip()

    client_name = input(
        "GhostNet node name: "
    ).strip()

    destination = input(
        "Destination node: "
    ).strip()

    interface_name_input = input(
        "TAP interface name: "
    ).strip()

    if not server_host:
        print("Server address cannot be empty.")
        return

    if not client_name:
        print("Node name cannot be empty.")
        return

    if not destination:
        print("Destination node cannot be empty.")
        return

    if not interface_name_input:
        print("TAP interface name cannot be empty.")
        return

    server_address = (
        server_host,
        SERVER_PORT,
    )

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    tap_fd = None
    stop_event = threading.Event()

    try:
        registration = encode_packet(
            packet_type=TYPE_REGISTER,
            source=client_name,
        )

        client_socket.sendto(
            registration,
            server_address,
        )

        tap_fd, interface_name = create_tap(
            interface_name_input
        )

        print(
            f"Created TAP interface: "
            f"{interface_name}"
        )

        receiver_thread = threading.Thread(
            target=receive_packets,
            args=(
                client_socket,
                tap_fd,
            ),
            daemon=True,
        )

        heartbeat_thread = threading.Thread(
            target=send_heartbeats,
            args=(
                client_socket,
                server_address,
                client_name,
                stop_event,
            ),
            daemon=True,
        )

        receiver_thread.start()
        heartbeat_thread.start()

        print(
            f"Tunneling Ethernet frames "
            f"to '{destination}'"
        )

        while True:
            frame = os.read(
                tap_fd,
                65535,
            )

            packet = encode_packet(
                packet_type=TYPE_FRAME,
                source=client_name,
                destination=destination,
                payload=encode_frame(frame),
            )

            client_socket.sendto(
                packet,
                server_address,
            )

            print(
                f"[SENT FRAME] "
                f"{len(frame)} bytes"
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
                server_address,
            )
        except OSError:
            pass

        if tap_fd is not None:
            os.close(tap_fd)

        client_socket.close()


if __name__ == "__main__":
    main()
