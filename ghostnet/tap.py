import fcntl
import os
import struct


TUN_DEVICE = "/dev/net/tun"

TUNSETIFF = 0x400454CA

IFF_TAP = 0x0002
IFF_NO_PI = 0x1000


def create_tap(interface_name="ghost0"):
    tap = os.open(
        TUN_DEVICE,
        os.O_RDWR,
    )

    request = struct.pack(
        "16sH",
        interface_name.encode("utf-8"),
        IFF_TAP | IFF_NO_PI,
    )

    result = fcntl.ioctl(
        tap,
        TUNSETIFF,
        request,
    )

    actual_name = (
        result[:16]
        .split(b"\x00", 1)[0]
        .decode("utf-8")
    )

    return tap, actual_name


def main():
    tap, interface_name = create_tap()

    print(
        f"Created TAP interface: "
        f"{interface_name}"
    )

    print(
        "Waiting for Ethernet frames..."
    )

    while True:
        frame = os.read(
            tap,
            65535,
        )

        print(
            f"Received Ethernet frame: "
            f"{len(frame)} bytes"
        )


if __name__ == "__main__":
    main()