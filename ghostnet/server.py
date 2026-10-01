import socket

from ghostnet.protocol import (
    TYPE_ERROR,
    TYPE_MESSAGE,
    TYPE_REGISTER,
    ProtocolError,
    decode_packet,
    encode_packet,
)


HOST = "0.0.0.0"
PORT = 9000

clients = {}


def handle_registration(packet, address):
    client_name = packet["source"]

    if not client_name:
        raise ProtocolError(
            "Registration packet requires a source"
        )

    clients[client_name] = address

    print(
        f"[REGISTERED] {client_name} "
        f"at {address[0]}:{address[1]}"
    )


def handle_message(server_socket, packet, address):
    source = packet["source"]
    destination = packet["destination"]
    payload = packet["payload"]

    if not destination:
        raise ProtocolError(
            "Message packet requires a destination"
        )

    if destination not in clients:
        error_packet = encode_packet(
            packet_type=TYPE_ERROR,
            source="server",
            destination=source,
            payload=f"Unknown client '{destination}'",
        )

        server_socket.sendto(
            error_packet,
            address,
        )

        return

    destination_address = clients[destination]

    forwarded_packet = encode_packet(
        packet_type=TYPE_MESSAGE,
        source=source,
        destination=destination,
        payload=payload,
    )

    server_socket.sendto(
        forwarded_packet,
        destination_address,
    )

    print(
        f"[FORWARD] {source} → {destination}: "
        f"{payload}"
    )


def main():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    server_socket.bind((HOST, PORT))

    print(
        f"GhostNet server listening "
        f"on UDP port {PORT}"
    )

    while True:
        data, address = server_socket.recvfrom(4096)

        try:
            packet = decode_packet(data)

            if packet["type"] == TYPE_REGISTER:
                handle_registration(
                    packet,
                    address,
                )

            elif packet["type"] == TYPE_MESSAGE:
                handle_message(
                    server_socket,
                    packet,
                    address,
                )

        except ProtocolError as exc:
            print(
                f"[INVALID PACKET] "
                f"{address}: {exc}"
            )


if __name__ == "__main__":
    main()