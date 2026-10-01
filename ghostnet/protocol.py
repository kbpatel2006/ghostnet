import json


PROTOCOL_VERSION = 1

TYPE_REGISTER = "register"
TYPE_MESSAGE = "message"
TYPE_ERROR = "error"


class ProtocolError(Exception):
    """Raised when a GhostNet packet is invalid."""
    pass


def encode_packet(
    packet_type,
    source=None,
    destination=None,
    payload=None,
):
    packet = {
        "version": PROTOCOL_VERSION,
        "type": packet_type,
        "source": source,
        "destination": destination,
        "payload": payload,
    }

    return json.dumps(packet).encode("utf-8")


def decode_packet(data):
    try:
        packet = json.loads(data.decode("utf-8"))

    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError("Packet is not valid JSON") from exc

    required_fields = {
        "version",
        "type",
        "source",
        "destination",
        "payload",
    }

    missing_fields = required_fields - packet.keys()

    if missing_fields:
        raise ProtocolError(
            f"Missing packet fields: {sorted(missing_fields)}"
        )

    if packet["version"] != PROTOCOL_VERSION:
        raise ProtocolError(
            f"Unsupported protocol version: {packet['version']}"
        )

    valid_types = {
        TYPE_REGISTER,
        TYPE_MESSAGE,
        TYPE_ERROR,
    }

    if packet["type"] not in valid_types:
        raise ProtocolError(
            f"Unknown packet type: {packet['type']}"
        )

    return packet