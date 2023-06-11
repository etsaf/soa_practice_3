from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChatRequest(_message.Message):
    __slots__ = ["sender", "session", "text", "topic"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    sender: str
    session: int
    text: str
    topic: str
    def __init__(self, session: _Optional[int] = ..., sender: _Optional[str] = ..., topic: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ["message", "session"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    message: str
    session: int
    def __init__(self, message: _Optional[str] = ..., session: _Optional[int] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class KillRequest(_message.Message):
    __slots__ = ["sender", "session", "victim"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    VICTIM_FIELD_NUMBER: _ClassVar[int]
    sender: str
    session: int
    victim: int
    def __init__(self, session: _Optional[int] = ..., sender: _Optional[str] = ..., victim: _Optional[int] = ...) -> None: ...

class UpdateReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ["name", "session"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    session: int
    def __init__(self, session: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
