# GhostNet Architecture

## Goal

GhostNet creates a virtual Layer 2 network between machines connected over an IP network.

## v0.2 data path

```text
Linux host A
    |
 ghost0 TAP
    |
 raw Ethernet frame
    |
GhostNet tunnel client
    |
 Base64 + GhostNet JSON packet
    |
 UDP
    |
GhostNet server
    |
 UDP
    |
GhostNet tunnel client
    |
 raw Ethernet frame
    |
 ghost0 TAP
    |
Linux host B
```

The Linux TAP interface exposes Ethernet frames to userspace. GhostNet reads those frames, encodes them for transport, sends them through the UDP server, decodes them on the peer, and writes them back to the peer TAP interface.

## Protocol v1

Each control or data packet contains:

```text
version
type
source
destination
payload
```

Current packet types:

- register
- message
- error
- heartbeat
- disconnect
- frame

## Current limitation

v0.2 is point-to-point at the GhostNet layer. Each tunnel client is configured with a destination node. v0.3 will replace that behavior with MAC learning, broadcast flooding, and destination-MAC forwarding so the server behaves like a Layer 2 switch.
