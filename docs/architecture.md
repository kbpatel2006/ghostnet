# GhostNet Architecture

## Goal

GhostNet creates a virtual Layer 2 network between machines connected
over the Internet.

## Initial Architecture

Client A
   |
   | UDP
   |
GhostNet Server
   |
   | UDP
   |
Client B

## Future Architecture

TAP Interface
     |
GhostNet Client
     |
Encryption
     |
UDP Tunnel
     |
GhostNet Switch
     |
UDP Tunnel
     |
Decryption
     |
GhostNet Client
     |
TAP Interface