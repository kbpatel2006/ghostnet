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


def format_mac(raw_mac):
    return ":".join(
        f"{byte:02x}"
        for byte in raw_mac
    )


def parse_ethernet_frame(frame):
    if len(frame) < 14:
        raise ValueError(
            "Ethernet frame is too short"
        )

    destination_mac = frame[0:6]
    source_mac = frame[6:12]

    ether_type = struct.unpack(
        "!H",
        frame[12:14],
    )[0]

    return {
        "destination_mac": format_mac(
            destination_mac
        ),
        "source_mac": format_mac(
            source_mac
        ),
        "ether_type": ether_type,
        "payload": frame[14:],
    }


def ether_type_name(ether_type):
    known_types = {
        0x0800: "IPv4",
        0x0806: "ARP",
        0x86DD: "IPv6",
    }

    return known_types.get(
        ether_type,
        "Unknown",
    )


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

        try:
            parsed = parse_ethernet_frame(
                frame
            )

        except ValueError as exc:
            print(
                f"[INVALID FRAME] {exc}"
            )
            continue

        print()
        print(
            f"Frame size: "
            f"{len(frame)} bytes"
        )
        print(
            f"Source MAC: "
            f"{parsed['source_mac']}"
        )
        print(
            f"Destination MAC: "
            f"{parsed['destination_mac']}"
        )
        print(
            f"EtherType: "
            f"0x{parsed['ether_type']:04x}"
        )
        print(
            f"Protocol: "
            f"{ether_type_name(parsed['ether_type'])}"
        )


if __name__ == "__main__":
    main()