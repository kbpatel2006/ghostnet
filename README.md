# GhostNet

GhostNet is a Layer 2 overlay network built from scratch in Python. It uses Linux TAP interfaces and UDP tunneling so machines on separate hosts can exchange Ethernet frames as if they were on the same local network.

## Current architecture

```text
Linux host A
    |
 ghost0 TAP
    |
GhostNet tunnel client
    |
    | UDP
    v
GhostNet server
    |
    | UDP
    v
GhostNet tunnel client
    |
 ghost0 TAP
    |
Linux host B
```

GhostNet v0.2 has been tested across separate Linux VMs with ARP and ICMP traffic traversing the tunnel.

## Development environment

- Python 3
- Linux for TAP interface support
- `/dev/net/tun`
- `iproute2`
- `iputils-ping`
- `tcpdump`
- `pytest`

On macOS, development can be done in VS Code while the repository is mounted into Linux VMs such as Multipass instances.

## Tests

```bash
pytest -v
```

## Roadmap

- [x] v0.1 UDP communication, peer registration, structured packets, heartbeats
- [x] v0.2 Linux TAP networking and point-to-point Ethernet tunneling
- [ ] v0.3 MAC learning and virtual switching
- [ ] v0.4 encrypted transport
- [ ] v0.5 authenticated peers
- [ ] v0.6 replay protection
- [ ] v0.7 ACL firewall
- [ ] v0.8 security logging
- [ ] v0.9 CLI
- [ ] v1.0 first stable release

See [CHANGELOG.md](CHANGELOG.md) for completed milestones.
