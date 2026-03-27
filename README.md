# Distributed Node Health Monitor & Failover System (Python)

A distributed systems simulation built in Python demonstrating real-world disaster recovery concepts.

## Features
- Async heartbeat monitoring of multiple nodes simultaneously
- Automatic failover; promotes backup nodes when primaries fail
- Handles multiple simultaneous failures gracefully
- Real-time cluster status reporting every 5 seconds
- Critical alerting when no backup nodes remain

## Technologies
- Python 3.10+
- asyncio; concurrent heartbeat monitoring
- Object-oriented design; Node, Monitor, FailoverManager

## Run
```bash
python3 src/main.py
```

## Architecture
- **Node** — simulates a server sending heartbeats, can randomly fail
- **Monitor** — watches all nodes concurrently, detects failures within seconds
- **FailoverManager** — automatically promotes backup nodes on failure detection

## Use Case
Simulates the core of a Disaster Recovery as a Service (DRaaS) system — the same architecture used in enterprise BCDR solutions for automatic failover and business continuity.
