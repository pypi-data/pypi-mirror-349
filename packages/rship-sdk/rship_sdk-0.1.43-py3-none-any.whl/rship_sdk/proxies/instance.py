from .target import TargetProxy, TargetArgs
from .event_track import EventTrackProxy, EventTrackArgs
from ..models import TargetStatusEnum, Instance, InstanceStatusEnum, Machine

class InstanceArgs():
    def __init__(self, name: str, code: str, service_id: str, cluster_id: str, 
                 color: str, machine_id: str, message: str):
        self.name = name
        self.code = code
        self.service_id = service_id
        self.cluster_id = cluster_id
        self.machine_id = machine_id
        self.color = color
        self.message = message

class InstanceProxy():
    def __init__(self, args: InstanceArgs, client):
        self.args = args
        self.client = client
        self.targets = {}
        self.event_tracks = {}
  
    async def add_target(self, args: TargetArgs):
        target = TargetProxy(self, args, self.client)
        await target.save(TargetStatusEnum.Online)

        self.targets[target.id()] = target
        return target
    
    async def add_event_track(self, args: EventTrackArgs):
        event_track = EventTrackProxy(self, args, self.client)
        await event_track.save()

        self.event_tracks[event_track.id()] = event_track
        return event_track

    async def save(self, status: InstanceStatusEnum):
        instance = Instance(
            id=self.id(),
            name=self.args.name,
            service_id=self.args.service_id,
            service_type_code=self.args.code,
            cluster_id=self.args.cluster_id,
            machine_id=self.args.machine_id,
            color=self.args.color,
            message=self.args.message,
            status=status,
        )

        machine = Machine(
            name=self.args.machine_id,
            # hash=generate_hash()
        )
        # if instance.id not in self.client.instances or self.client.instances[instance.id].hash != instance.hash:
        await self.client.set_data(instance, 'Instance')

        # if machine.id not in self.client.machines or self.client.machines[machine.id].hash != machine.hash:
        await self.client.set_data(machine, 'Machine')

        for target in self.targets.values():
            await target.save(TargetStatusEnum.Online)

        print("Targets saved")
      
    async def set_status(self, status: InstanceStatusEnum):
        await self.save(status)

    def id(self) -> str:
        return f"{self.args.service_id}:{self.args.machine_id}"
    