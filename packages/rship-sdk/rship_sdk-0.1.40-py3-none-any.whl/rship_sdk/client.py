import json
import websockets
import traceback

from typing import Any, Callable, Dict, Coroutine
from myko import MEvent, MEventType, MCommand, WSMEvent, WSMCommand

from .models import Target, Action, Emitter, Pulse,  Machine, Alert, InstanceStatusEnum, TargetStatus, EventTrack
from .utils import generate_hash, get_current_timestamp

from .proxies.instance import InstanceProxy, InstanceArgs

class RshipExecClient:
    def __init__(self, rship_host: str, rship_port: int):
        self.rship_host = rship_host
        self.rship_port = rship_port
        self.is_connected = False
        self.websocket = None
        self.targets: Dict[str, Target] = {}
        self.target_statuses: Dict[str, TargetStatus] = {}
        self.actions: Dict[str, Action] = {}
        self.emitters: Dict[str, Emitter] = {}
        self.instances: Dict[str, InstanceProxy] = {}
        self.machines: Dict[str, Machine] = {}
        self.alerts: Dict[str, Alert] = {}
        self.handlers: Dict[str, Coroutine[Action, Any, None]] = {}
        self.event_tracks: Dict[str, EventTrack] = {}

    ##############################
    # Websockets
    ##############################

    async def connect(self):
        uri = f"ws://{self.rship_host}:{self.rship_port}/myko"
        print(f"Attempting to connect to {uri}")
        try:
            self.websocket = await websockets.connect(uri)
            print("Connected to Rship server successfully.")
            self.is_connected = True
        except Exception as e:
            print(f"Failed to connect to rship - {e}")

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            print("Disconnected from Rship server")
            self.is_connected = False

    async def send_event(self, event: MEvent):
        try: 
            await self.websocket.send(json.dumps(WSMEvent(event).__dict__))
        except TypeError as e:
            print(f"Failed to send event: TypeError - {e}")
            traceback.print_exc()

    async def send_command(self, command: MCommand):
        try:
            await self.websocket.send(json.dumps(WSMCommand(command).__dict__))
        except ConnectionError as e:
            print(f"Failed to send command: ConnectionError - {e}")

    async def receive_messages(self):
        while self.websocket:
            try:
                message = await self.websocket.recv()
                # print(f"Received message: {message}")
                await self.handle_message(message)
            except websockets.ConnectionClosed:
                await self.disconnect()

    async def handle_message(self, message: str):
        data = json.loads(message)
        # print(f"Received command: {data}")
        if data["event"] == "ws:m:command":
            command_data = data["data"]
            command_id = command_data["commandId"]
            if command_id == "ExecTargetAction":
                action_id = command_data["command"]["action"]["id"]
                if action_id in self.actions:
                    action = self.actions[action_id]
                    handler = self.handlers.get(action_id)
                    if handler:
                       await handler(action, command_data["command"]["data"])

    ##############################
    # RSHIP API
    ##############################

    async def set_data(self, item: Any, item_type: str):
        event = MEvent(item=item, item_type=item_type, change_type=MEventType.SET,
                       created_at=get_current_timestamp(), tx=generate_hash())
        await self.send_event(event)


    async def delete_data(self, item: Any, item_type: str):
        event = MEvent(item=item, item_type=item_type, change_type=MEventType.DEL,
                       created_at=get_current_timestamp(), tx=generate_hash())
        await self.send_event(event)


    async def add_instance(self, args: InstanceArgs):
        instance_proxy = InstanceProxy(args=args, 
                                       client=self)
        await instance_proxy.save(InstanceStatusEnum.Available)

        self.instances[instance_proxy.id()] = instance_proxy
        return instance_proxy


    async def pulse_emitter(self, service_short_id: str, target_short_id: str, emitter_short_id: str, data: Any):
        full_emitter_id = f"{service_short_id}:{target_short_id}:{emitter_short_id}"
        pulse = Pulse(name="", emitter_id=full_emitter_id, data=data)
        await self.set_data(pulse, 'Pulse')
