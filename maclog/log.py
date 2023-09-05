import dataclasses
import datetime
import json
import subprocess
import uuid
from enum import Enum
from pathlib import Path
from typing import List, Mapping, Optional, Union


class LogLevel(Enum):
    DEFAULT = 'default'
    INFO = 'info'
    DEBUG = 'debug'


@dataclasses.dataclass
class Frame:
    image_uuid: str
    image_offset: int

    @classmethod
    def from_dict(cls, d: Mapping) -> 'Frame':
        return cls(image_uuid=d['imageUUID'], image_offset=d['imageOffset'])


@dataclasses.dataclass
class Backtrace:
    frames: List[Frame]

    @classmethod
    def from_dict(cls, d: Mapping) -> 'Backtrace':
        return cls(frames=[Frame.from_dict(frame) for frame in d['frames']])


@dataclasses.dataclass
class LogEntry:
    trace_id: int
    event_message: str
    event_type: str
    format_string: str
    activity_identifier: int
    subsystem: str
    category: str
    thread_id: int
    sender_image_uuid: str
    backtrace: Backtrace
    process_image_path: Path
    timestamp: datetime.datetime
    sender_image_path: Path
    mach_timestamp: int
    process_image_uuid: Optional[uuid.UUID]
    process_id: int
    sender_program_counter: int
    parent_activity_identifier: int
    timezone_name: str
    message_type: Optional[str] = None
    source: Optional[str] = None
    boot_uuid: Optional[uuid.UUID] = None

    @classmethod
    def from_json(cls, entry: bytes) -> 'LogEntry':
        entry = json.loads(entry)
        return cls(trace_id=entry['traceID'],
                   event_message=entry['eventMessage'],
                   event_type=entry['eventType'],
                   source=entry.get('source'),
                   format_string=entry['formatString'],
                   activity_identifier=entry['activityIdentifier'],
                   subsystem=entry['subsystem'],
                   category=entry['category'],
                   thread_id=entry['threadID'],
                   sender_image_uuid=entry['senderImageUUID'],
                   backtrace=Backtrace.from_dict(entry['backtrace']),
                   boot_uuid=entry['bootUUID'],
                   process_image_path=Path(entry['processImagePath']),
                   timestamp=entry['timestamp'],
                   sender_image_path=Path(entry['senderImagePath']),
                   mach_timestamp=entry['machTimestamp'],
                   message_type=entry.get('messageType'),
                   process_image_uuid=entry['processImageUUID'],
                   process_id=entry['processID'],
                   sender_program_counter=entry['senderProgramCounter'],
                   parent_activity_identifier=entry['parentActivityIdentifier'],
                   timezone_name=entry['timezoneName'])


def get_logger(predicate: Optional[str] = None, level: Union[LogLevel, str] = LogLevel.DEBUG):
    args = ['log', 'stream', '--level', str(level), '--style', 'ndjson']
    if predicate is not None:
        args += ['--predicate', predicate]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    while True:
        yield LogEntry.from_json(proc.stdout.readline())
