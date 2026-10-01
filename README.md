# GhostNet

GhostNet is a secure Layer 2 overlay network built from scratch.

The goal is to allow machines across the Internet to communicate
as though they are connected to the same local Ethernet network.

## Architecture

Linux TAP Interface
        |
GhostNet Client
        |
       UDP
        |
GhostNet Switch
        |
       UDP
        |
GhostNet Client
        |
Linux TAP Interface

## Roadmap

- [ ] v0.1 UDP communication
- [ ] v0.2 TAP networking
- [ ] v0.3 MAC learning and switching
- [ ] v0.4 encrypted transport
- [ ] v0.5 authenticated peers
- [ ] v0.6 replay protection
- [ ] v0.7 ACL firewall
- [ ] v0.8 security logging
- [ ] v0.9 CLI
- [ ] v1.0 first stable release