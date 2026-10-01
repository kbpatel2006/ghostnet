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


HOST = "0.0.0.0"
PORT = 9000

CLIENT_TIMEOUT = 15
CLEANUP_INTERVAL = 5

clients = {}
clients_lock = threading.Lock()


def register_client(packet, address):
    client_name = packet["source"]

    if not client_name:
        raise ProtocolError(
            "Registration packet requires a source"
        )

    with clients_lock:
        clients[client_name] = {
            "address": address,
            "last_seen": time.monotonic(),
        }

    print(
        f"[REGISTERED] {client_name} "
        f"at {address[0]}:{address[1]}"
    )


def update_heartbeat(packet, address):
    client_name = packet["source"]

    if not client_name:
        return

    with clients_lock:
        client = clients.get(client_name)

        if client is None:
            return

        if client["address"] != address:
            return

        client["last_seen"] = time.monotonic()


def disconnect_client(packet, address):
    client_name = packet["source"]

    if not client_name:
        return

    with clients_lock:
        client = clients.get(client_name)

        if client is None:
            return

        if client["address"] != address:
            return

        del clients[client_name]

    print(f"[DISCONNECTED] {client_name}")


def handle_message(server_socket, packet, address):
    source = packet["source"]
    destination = packet["destination"]
    payload = packet["payload"]

    if not source:
        raise ProtocolError(
            "Message packet requires a source"
        )

    if not destination:
        raise ProtocolError(
            "Message packet requires a destination"
        )

    with clients_lock:
        source_client = clients.get(source)

        if (
            source_client is None
            or source_client["address"] != address
        ):
            print(
                f"[REJECTED] Invalid source '{source}' "
                f"from {address}"
            )
            return

        source_client["last_seen"] = time.monotonic()

        destination_client = clients.get(destination)

        if destination_client:
            destination_address = (
                destination_client["address"]
            )
        else:
            destination_address = None

    if destination_address is None:
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


def cleanup_clients():
    while True:
        time.sleep(CLEANUP_INTERVAL)

        now = time.monotonic()
        expired = []

        with clients_lock:
            for name, client in clients.items():
                age = now - client["last_seen"]

                if age > CLIENT_TIMEOUT:
                    expired.append(name)

            for name in expired:
                del clients[name]

        for name in expired:
            print(
                f"[TIMEOUT] Removed inactive client: {name}"
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

    cleanup_thread = threading.Thread(
        target=cleanup_clients,
        daemon=True,
    )

    cleanup_thread.start()

    while True:
        data, address = server_socket.recvfrom(4096)

        try:
            packet = decode_packet(data)

            if packet["type"] == TYPE_REGISTER:
                register_client(
                    packet,
                    address,
                )

            elif packet["type"] == TYPE_MESSAGE:
                handle_message(
                    server_socket,
                    packet,
                    address,
                )

            elif packet["type"] == TYPE_HEARTBEAT:
                update_heartbeat(
                    packet,
                    address,
                )

            elif packet["type"] == TYPE_DISCONNECT:
                disconnect_client(
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