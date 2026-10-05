import os
import socket
import threading

from ghostnet.protocol import (
    TYPE_FRAME,
    TYPE_REGISTER,
    ProtocolError,
    decode_frame,
    decode_packet,
    encode_frame,
    encode_packet,
)

from ghostnet.tap import create_tap


SERVER_PORT = 9000


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


def main():
    server_host = input(
    "GhostNet server address: "
    ).strip()

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    client_name = input(
        "GhostNet node name: "
    ).strip()

    destination = input(
        "Destination node: "
    ).strip()

    interface_name_input = input(
        "TAP interface name: "
    ).strip()

    registration = encode_packet(
        packet_type=TYPE_REGISTER,
        source=client_name,
    )

    client_socket.sendto(
        registration,
        (
            server_host,
            SERVER_PORT,
        ),
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

    receiver_thread.start()

    print(
        f"Tunneling Ethernet frames "
        f"to '{destination}'"
    )

    while True:
        frame = os.read(
            tap_fd,
            65535,
        )

        encoded = encode_frame(
            frame
        )

        packet = encode_packet(
            packet_type=TYPE_FRAME,
            source=client_name,
            destination=destination,
            payload=encoded,
        )

        client_socket.sendto(
            packet,
            (
                server_host,
                SERVER_PORT,
            ),
        )

        print(
            f"[SENT FRAME] "
            f"{len(frame)} bytes"
        )


if __name__ == "__main__":
    main()