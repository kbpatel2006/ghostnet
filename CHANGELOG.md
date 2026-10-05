# Changelog

## v0.2.1

- Restored the complete v0.2 tunnel implementation on the main development line
- Added tunnel heartbeats so idle TAP peers are not removed by server timeout
- Added graceful tunnel disconnect handling
- Increased server receive capacity for encapsulated Ethernet frames
- Added validation for frame payload encoding
- Added protocol and Ethernet frame parsing tests
- Added GitHub Actions compile, import, and test checks
- Added repository ignore rules for virtual environments, Python caches, macOS metadata, and private key files
- Updated README and architecture documentation through v0.2

## v0.2.0

- Added Linux TAP interface support through `/dev/net/tun`
- Added Ethernet frame parsing for source MAC, destination MAC, and EtherType
- Added Base64 transport for raw Ethernet frames inside GhostNet protocol packets
- Added UDP tunneling between GhostNet nodes
- Added received-frame injection back into TAP interfaces
- Added support for a remote GhostNet server address
- Verified ARP and ICMP traffic across separate Linux VMs

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
