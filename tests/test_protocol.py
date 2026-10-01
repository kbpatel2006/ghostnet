import pytest

from ghostnet.protocol import (
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