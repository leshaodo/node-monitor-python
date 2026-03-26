import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.node import Node
from src.monitor import Monitor
from src.failover_manager import FailoverManager

async def main():
    print("=" * 60)
    print("  Distributed Node Health Monitor & Failover System")
    print("=" * 60)

    nodes = [
        Node("node-primary-1"),
        Node("node-primary-2"),
        Node("node-primary-3"),
        Node("node-backup-1", is_backup=True),
        Node("node-backup-2", is_backup=True),
    ]

    failover_manager = FailoverManager(nodes)
    monitor = Monitor(nodes, failover_manager)

    print(f"\nStarting cluster with {len(nodes)} nodes...")
    print("Primary nodes: node-primary-1, node-primary-2, node-primary-3")
    print("Backup nodes:  node-backup-1, node-backup-2")
    print("\nMonitoring started. Press Ctrl+C to stop.\n")

    tasks = []
    for node in nodes:
        if not node.is_backup:
            tasks.append(asyncio.create_task(node.send_heartbeat()))

    tasks.append(asyncio.create_task(monitor.check_nodes()))
    tasks.append(asyncio.create_task(monitor.print_status()))

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("\nShutting down monitor...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSystem stopped by user.")
