from ..models import EventTrack, EventTrackLane, TimeMode, Keyframe, ConcreteSchemaType
from typing import List, Dict
from uuid import uuid4

class EventTrackArgs:
    def __init__(self, name: str, short_id: str, time_mode: TimeMode):
        self.name = name
        self.short_id = short_id
        self.time_mode = time_mode


class KeyframeArgs:
    def __init__(self, time: float, data: any):
        self.time = time
        self.data = data
        

class EventTrackLaneArgs:
    def __init__(self, short_id: str, name: str, type: ConcreteSchemaType, keys: List[KeyframeArgs]):
        self.short_id = short_id
        self.name = name
        self.type = type
        self.keys = keys


class EventTrackProxy:
    def __init__(self, instance, args: EventTrackArgs, client):
        self.client = client
        self.args = args
        self.instance = instance
        self.lanes: Dict[str, EventTrackLaneProxy] = {}
   
    def id(self) -> str:
        return f"{self.instance.args.service_id}:{self.args.short_id}"
    
    async def add_lane(self, args: EventTrackLaneArgs) -> 'EventTrackLaneProxy':
        p = EventTrackLaneProxy(self.instance, self.client, args, self)
        self.lanes[p.id()] = p
        await self.save() # save EventTrackProxy
        await p.save() # save EventTrackLaneProxy
        return p
    
    async def save(self):
        event_track = EventTrack(
            id=self.id(),
            name=self.args.name,
            time_mode=self.args.time_mode.__dict__,
            service_id=self.instance.args.service_id,
        )

        if event_track.id not in self.client.event_tracks or self.client.event_tracks[event_track.id] != event_track.hash:
            await self.client.set_data(event_track, 'EventTrack')
            self.client.event_tracks[event_track.id] = event_track

    async def save_all(self):
        await self.save()
        for lane in self.lanes.values():
            await lane.save()


class EventTrackLaneProxy:
    def __init__(self, instance, client, args: EventTrackLaneArgs, track: EventTrackProxy):
        self.client = client
        self.args = args
        self.track = track
        self.sent = {}

    def id(self) -> str:
        return f"{self.track.id()}:{self.args.short_id}"
    
    async def save(self):
        tx = str(uuid4())

        frames = [
            Keyframe(
                id=f"{self.id}:{key.time}",
                event_track_id=self.track.id(),
                data_type=self.args.type,
                layer_id=self.id(),
                time=key.time,
                value=key.data,
            )
            for key in self.args.keys
        ]

        grouped_by_lanes = {}
        for frame in frames:
            if frame.layerId not in grouped_by_lanes:
                grouped_by_lanes[frame.layerId] = []
            grouped_by_lanes[frame.layerId].append(frame)

        lanes = [
            EventTrackLane(
                id=layer_id,
                name=self.args.name,
                event_track_id=self.track.id(),
                type=self.args.type,
            )
            for layer_id in grouped_by_lanes
        ]

        for lane in lanes:
            await self.client.set_data(lane, 'EventTrackLayer')

        to_delete = dict(self.sent)
        for frame in frames:
            if frame.id in to_delete:
                to_delete.pop(frame.id)

        self.sent.clear()

        for frame in frames:
            self.sent[frame.id] = frame
            await self.client.set_data(frame, 'Keyframe')
        
        for frame_id, frame in to_delete:
            await self.client.delete_data(frame, 'Keyframe')

        self.sent.clear()