import struct

import pytest

from ghostnet.protocol import (
    TYPE_DISCONNECT,
    TYPE_FRAME,
    TYPE_HEARTBEAT,
    TYPE_MESSAGE,
    ProtocolError,
    decode_frame,
    decode_packet,
    encode_frame,
    encode_packet,
)
from ghostnet.tap import parse_ethernet_frame


def test_encode_decode_message():
    encoded = encode_packet(
        packet_type=TYPE_MESSAGE,
        source="alice",
        destination="bob",
        payload="hello",
    )

    packet = decode_packet(encoded)

    assert packet["version"] == 1
    assert packet["type"] == TYPE_MESSAGE
    assert packet["source"] == "alice"
    assert packet["destination"] == "bob"
    assert packet["payload"] == "hello"


def test_heartbeat_packet():
    encoded = encode_packet(
        packet_type=TYPE_HEARTBEAT,
        source="alice",
    )

    packet = decode_packet(encoded)

    assert packet["type"] == TYPE_HEARTBEAT
    assert packet["source"] == "alice"


def test_disconnect_packet():
    encoded = encode_packet(
        packet_type=TYPE_DISCONNECT,
        source="alice",
    )

    packet = decode_packet(encoded)

    assert packet["type"] == TYPE_DISCONNECT
    assert packet["source"] == "alice"


def test_frame_packet():
    encoded = encode_packet(
        packet_type=TYPE_FRAME,
        source="node-a",
        destination="node-b",
        payload=encode_frame(b"frame-data"),
    )

    packet = decode_packet(encoded)

    assert packet["type"] == TYPE_FRAME
    assert packet["source"] == "node-a"
    assert packet["destination"] == "node-b"
    assert decode_frame(packet["payload"]) == b"frame-data"


def test_invalid_json():
    with pytest.raises(ProtocolError):
        decode_packet(b"this is not json")


def test_invalid_version():
    data = (
        b'{"version":999,'
        b'"type":"message",'
        b'"source":"alice",'
        b'"destination":"bob",'
        b'"payload":"hello"}'
    )

    with pytest.raises(ProtocolError):
        decode_packet(data)


def test_json_array_rejected():
    with pytest.raises(ProtocolError):
        decode_packet(b'["hello"]')


def test_unknown_packet_type():
    data = (
        b'{"version":1,'
        b'"type":"random",'
        b'"source":"alice",'
        b'"destination":null,'
        b'"payload":null}'
    )

    with pytest.raises(ProtocolError):
        decode_packet(data)


def test_frame_encoding_round_trip():
    original = b"\xff\xff\xff\xff\xff\xffhello"

    encoded = encode_frame(original)
    decoded = decode_frame(encoded)

    assert decoded == original


def test_invalid_frame_encoding():
    with pytest.raises(ProtocolError):
        decode_frame("not valid base64!!!")


def test_parse_ethernet_frame():
    destination = bytes.fromhex("ffffffffffff")
    source = bytes.fromhex("001122334455")
    ether_type = struct.pack("!H", 0x0806)
    payload = b"arp-payload"

    parsed = parse_ethernet_frame(
        destination + source + ether_type + payload
    )

    assert parsed["destination_mac"] == "ff:ff:ff:ff:ff:ff"
    assert parsed["source_mac"] == "00:11:22:33:44:55"
    assert parsed["ether_type"] == 0x0806
    assert parsed["payload"] == payload


def test_short_ethernet_frame_rejected():
    with pytest.raises(ValueError):
        parse_ethernet_frame(b"too-short")
