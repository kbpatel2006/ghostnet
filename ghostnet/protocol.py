import base64
import binascii
import json


PROTOCOL_VERSION = 1

TYPE_REGISTER = "register"
TYPE_MESSAGE = "message"
TYPE_ERROR = "error"
TYPE_HEARTBEAT = "heartbeat"
TYPE_DISCONNECT = "disconnect"
TYPE_FRAME = "frame"


class ProtocolError(Exception):
    """Raised when a GhostNet packet is invalid."""



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

    if not isinstance(packet, dict):
        raise ProtocolError("Packet must be a JSON object")

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
        TYPE_HEARTBEAT,
        TYPE_DISCONNECT,
        TYPE_FRAME,
    }

    if packet["type"] not in valid_types:
        raise ProtocolError(
            f"Unknown packet type: {packet['type']}"
        )

    return packet


def encode_frame(frame):
    if not isinstance(frame, bytes):
        raise ProtocolError("Frame must be bytes")

    return base64.b64encode(frame).decode("ascii")


def decode_frame(encoded_frame):
    if not isinstance(encoded_frame, str):
        raise ProtocolError("Encoded frame must be a string")

    try:
        return base64.b64decode(
            encoded_frame,
            validate=True,
        )
    except (binascii.Error, ValueError) as exc:
        raise ProtocolError(
            "Invalid frame encoding"
        ) from exc
