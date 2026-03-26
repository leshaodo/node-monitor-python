import asyncio
import random
import logging
from datetime import datetime

class Node:
    def __init__(self, node_id: str, is_backup: bool = False):
        self.node_id = node_id
        self.is_backup = is_backup
        self.is_alive = True
        self.last_heartbeat = datetime.now()
        self.heartbeat_interval = 1.0
        self.fail_probability = 0.05

    async def send_heartbeat(self):
        while self.is_alive:
            await asyncio.sleep(self.heartbeat_interval)
            if random.random() < self.fail_probability:
                self.is_alive = False
                print(f"[{datetime.now().strftime('%H:%M:%S')}] NODE FAILURE: {self.node_id} has gone down")
                return
            self.last_heartbeat = datetime.now()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] HEARTBEAT: {self.node_id} is alive")

    def activate(self):
        self.is_alive = True
        self.is_backup = False
        self.last_heartbeat = datetime.now()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ACTIVATED: {self.node_id} is now a primary node")

    def get_status(self):
        return {
            "node_id": self.node_id,
            "is_alive": self.is_alive,
            "is_backup": self.is_backup,
            "last_heartbeat": self.last_heartbeat.strftime('%H:%M:%S')
        }
