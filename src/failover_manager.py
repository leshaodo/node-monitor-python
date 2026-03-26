import asyncio
from datetime import datetime

class FailoverManager:
    def __init__(self, nodes: list):
        self.nodes = nodes
        self.failover_count = 0
        self.handled_failures = set()

    async def trigger_failover(self, failed_node):
        if failed_node.node_id in self.handled_failures:
            return

        self.handled_failures.add(failed_node.node_id)
        failed_node.is_alive = False
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FAILOVER: Starting recovery for {failed_node.node_id}")

        backup = self.find_backup()
        if backup:
            await asyncio.sleep(0.5)
            backup.activate()
            self.failover_count += 1
            print(f"[{datetime.now().strftime('%H:%M:%S')}] FAILOVER COMPLETE: {backup.node_id} promoted after {failed_node.node_id} failed | Total failovers: {self.failover_count}")
            asyncio.create_task(backup.send_heartbeat())
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] CRITICAL: No backup nodes available for failover!")

    def find_backup(self):
        for node in self.nodes:
            if node.is_backup and node.is_alive:
                return node
        return None
