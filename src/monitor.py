import asyncio
from datetime import datetime
from src.node import Node

class Monitor:
    def __init__(self, nodes: list, failover_manager):
        self.nodes = nodes
        self.failover_manager = failover_manager
        self.check_interval = 2.0
        self.timeout_threshold = 3.0

    async def check_nodes(self):
        while True:
            await asyncio.sleep(self.check_interval)
            now = datetime.now()
            for node in self.nodes:
                if not node.is_backup:
                    seconds_since = (now - node.last_heartbeat).total_seconds()
                    if not node.is_alive or seconds_since > self.timeout_threshold:
                        print(f"[{now.strftime('%H:%M:%S')}] ALERT: {node.node_id} is unresponsive — triggering failover")
                        await self.failover_manager.trigger_failover(node)

    async def print_status(self):
        while True:
            await asyncio.sleep(5.0)
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] --- CLUSTER STATUS ---")
            for node in self.nodes:
                status = node.get_status()
                role = "BACKUP" if status["is_backup"] else "PRIMARY"
                state = "ALIVE" if status["is_alive"] else "DOWN"
                print(f"  {status['node_id']} | {role} | {state} | Last heartbeat: {status['last_heartbeat']}")
            print()
