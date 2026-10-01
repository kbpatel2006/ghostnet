import pytest

from ghostnet.protocol import (
    TYPE_DISCONNECT,
    TYPE_HEARTBEAT,
    TYPE_MESSAGE,
    ProtocolError,
    decode_packet,
    encode_packet,
)


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


def test_invalid_json():
    data = b"this is not json"

    with pytest.raises(ProtocolError):
        decode_packet(data)


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
    data = b'["hello"]'

    with pytest.raises(ProtocolError):
        decode_packet(data)


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