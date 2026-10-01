import socket

HOST = '0.0.0.0'
PORT = 9000

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print("ghostnet server listening on port", PORT)

    while True:
        data, address = server_socket.recvfrom(4096)

        message = data.decode("utf-8")

        print(f"\nReceived from {address[0]}:{address[1]}")
        print(f"Message: {message}")

if __name__ == "__main__":
    main()
