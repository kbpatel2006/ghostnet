# Changelog

## v0.2.0

- Added Linux TAP interface support through `/dev/net/tun`
- Added Ethernet frame parsing for source MAC, destination MAC, and EtherType
- Added Base64 transport for raw Ethernet frames inside GhostNet protocol packets
- Added UDP tunneling between GhostNet nodes
- Added received-frame injection back into TAP interfaces
- Added support for a remote GhostNet server address
- Added tunnel heartbeats and graceful disconnect handling
- Verified ARP and ICMP traffic across separate Linux VMs
- Added protocol and Ethernet parsing tests

## v0.1.0

- Added UDP client/server communication
- Added peer registration and forwarding
- Added structured JSON packet protocol
- Added protocol version validation
- Added heartbeat-based peer health checks
- Added graceful disconnect handling
- Added stale-peer cleanup
- Added basic source-address validation
- Added protocol tests
