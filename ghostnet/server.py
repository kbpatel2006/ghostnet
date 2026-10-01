import socket


HOST = "0.0.0.0"
PORT = 9000

clients = {}


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print(f"ghostnet server listening on UDP port {PORT}")

    while True:
        data, address = server_socket.recvfrom(4096)

        message = data.decode("utf-8")

        # Registration message:
        # REGISTER:kush
        if message.startswith("REGISTER:"):
            client_name = message.split(":", 1)[1].strip()

            clients[client_name] = address

            print(
                f"[REGISTERED] {client_name} "
                f"at {address[0]}:{address[1]}"
            )

            continue

        # Normal message format:
        # SEND:client2:hello
        if message.startswith("SEND:"):
            parts = message.split(":", 2)

            if len(parts) != 3:
                print(f"[INVALID] {message}")
                continue

            _, destination, payload = parts

            if destination not in clients:
                error = f"ERROR:Unknown client '{destination}'"

                server_socket.sendto(
                    error.encode("utf-8"),
                    address,
                )

                continue

            destination_address = clients[destination]

            forwarded_message = f"MESSAGE:{payload}"

            server_socket.sendto(
                forwarded_message.encode("utf-8"),
                destination_address,
            )

            print(
                f"[FORWARD] {address} → {destination} "
                f"({destination_address})"
            )


if __name__ == "__main__":
    main()