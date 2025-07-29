from enum import Enum
from typing import Union, List, Optional, Any
from myko import MItem, MCommand, Schema
from .utils import generate_hash

class Target(MItem):
    def __init__(self, id: str, name: str,
                 sub_targets: List[str], parent_targets: List[str], service_id: str,
                 bg_color: str, fg_color: str, last_updated: str, category: str, root_level: bool):
        super().__init__(id, name)

        self.category = category
        self.bgColor = bg_color
        self.fgColor = fg_color
        self.parentTargets = parent_targets
        self.subTargets = sub_targets
        self.serviceId = service_id
        self.lastUpdated = last_updated
        self.rootLevel = root_level
        # self.hash = str(uuid())


class TargetStatusEnum(Enum):
    Online = 'online'
    Offline = 'offline'


class TargetStatus(MItem):
    def __init__(self, id: str, name: str, target_id: str, status: TargetStatusEnum, last_updated: str, instance_id: str):
        super().__init__(id, name)

        self.targetId = target_id
        self.status = status.value
        self.lastUpdated = last_updated
        self.instanceId = instance_id
        # self.hash = generate_hash()


class Action(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)

        self.schema = schema
        self.targetId = target_id
        self.serviceId = service_id
        # self.hash = generate_hash()


class Emitter(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)

        self.schema = schema
        self.targetId = target_id
        self.serviceId = service_id
        # self.hash = generate_hash()


class Pulse(MItem):
    def __init__(self, name: str, emitter_id: str, data: Any):
        super().__init__(emitter_id, name)

        self.emitterId = emitter_id
        self.data = data
        # self.hash = generate_hash()


class KeyframeData():
    type: str

class NumberKeyframeData(KeyframeData):
    def __init__(self, value: float, fade_in: Optional[float] = None, curve_id: Optional[str] = None):
        self.type = 'number'
        self.value = value
        self.fade_in = fade_in
        self.curve_id = curve_id

class IntegerKeyframeData(KeyframeData):
    def __init__(self, value: int, fade_in: Optional[float] = None, curve_id: Optional[str] = None):
        self.type = 'integer'
        self.value = value
        self.fade_in = fade_in
        self.curve_id = curve_id



class StringKeyframeData(KeyframeData):
    def __init__(self, value: str):
        self.type = 'string'
        self.value = value

class BooleanKeyframeData(KeyframeData):
    def __init__(self, value: bool):
        self.type = 'boolean'
        self.value = value


class GlobalVariableKeyframeData(KeyframeData):
    def __init__(self, value: str, fade_in: Optional[float] = None, curve_id: Optional[str] = None):
        self.type = 'global_variable'
        self.value = value
        self.fade_in = fade_in
        self.curve_id = curve_id


class SceneOutputKeyframeData(KeyframeData):
    def __init__(self, value: str, fade_in: Optional[float] = None, curve_id: Optional[str] = None):
        self.type = 'scene_output'
        self.value = value
        self.fade_in = fade_in
        self.curve_id = curve_id


class NullKeyframeData(KeyframeData):
    def __init__(self):
        self.type = 'null'
        self.value = None

    


class TimeMode():
    type: str


class ClockTimeMode(TimeMode):
    def __init__(self):
        self.type = 'clock'


class BeatTimeMode(TimeMode):
    def __init__(self, measure: int):
        self.type = 'beat'
        self.measure = measure


class FrameTimeMode(TimeMode):
    def __init__(self, rate: float):
        self.type = 'frame'
        self.rate = rate


class EventTrack(MItem):
    def __init__(self, id: str, name: str, time_mode: TimeMode, service_id: str):
        super().__init__(id, name)
        self.timeMode = time_mode
        self.sourceMode = {'type': 'sourced', 'service_id': service_id}


class ConcreteSchemaType(Enum):
    Null = 'null'
    String = 'string'
    Number = 'number'
    Integer = 'integer'
    Boolean = 'boolean'
    Object = 'object'
    Array = 'array'
    Ref = 'ref'
    

class EventTrackLane(MItem):
    def __init__(self, id: str, name: str, event_track_id: str, type: ConcreteSchemaType):
        super().__init__(id, name)
        self.eventTrackId = event_track_id
        self.type = type.value
        

class Keyframe(MItem):
    def __init__(self, id: str, event_track_id: str, layer_id: str, time: int, data: KeyframeData):
        super().__init__(id, f"{time}")
        self.eventTrackId = event_track_id
        self.layerId = layer_id
        self.time = time
        self.data = data


class InstanceStatusEnum(Enum):
    Starting = 'Starting'
    Available = 'Available'
    Stopping = 'Stopping'
    Unavailable = 'Unavailable'
    Error = 'Error'


class Instance(MItem):
    def __init__(self, id: str, name: str, service_id: str, cluster_id: str, service_type_code: str,
                 status: InstanceStatusEnum, machine_id: str, color: str, message: str):
        super().__init__(id, name)

        self.serviceId = service_id
        self.serviceTypeCode = service_type_code
        self.clusterId = cluster_id
        self.machineId = machine_id
        self.color = color
        # self.hash = generate_hash()
        
        self.message = message
        self.status = status.value


class Machine(MItem):
    def __init__(self, name: str):
        super().__init__(name, name)

class ExecTargetAction(MCommand):
    def __init__(self, tx: str, createdAt: str, action: Action, data: any):
        super().__init__(tx, createdAt)

        self.action = action
        self.data = data
        self.hash = generate_hash()


class AlertLevel(Enum):
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


class AlertEntityType(Enum):
    TARGET = 'Target'
    ACTION = 'Action'
    PAYLOAD = 'Payload'
    INSTANCE = 'Instance'


class Alert(MItem):
    def __init__(self, entity_id: str, entity_type: AlertEntityType, instance_id: str,
                 level: AlertLevel, message: str, code: str):
        super().__init__(entity_id + instance_id, f"{entity_id}:{code}")
        self.entityId = entity_id
        self.entityType = entity_type.value
        self.instanceId = instance_id
        self.level = level.value
        self.message = message
        self.code = code
        # self.hash = generate_hash()