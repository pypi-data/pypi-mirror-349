from yeying.api.common import message_pb2 as _message_pb2
from yeying.api.common import code_pb2 as _code_pb2
from yeying.api.common import model_pb2 as _model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterServiceRequest(_message.Message):
    __slots__ = ("header", "body")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    header: _message_pb2.MessageHeader
    body: RegisterServiceRequestBody
    def __init__(self, header: _Optional[_Union[_message_pb2.MessageHeader, _Mapping]] = ..., body: _Optional[_Union[RegisterServiceRequestBody, _Mapping]] = ...) -> None: ...

class RegisterServiceRequestBody(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _model_pb2.ServiceMetadata
    def __init__(self, service: _Optional[_Union[_model_pb2.ServiceMetadata, _Mapping]] = ...) -> None: ...

class RegisterServiceResponse(_message.Message):
    __slots__ = ("header", "body")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    header: _message_pb2.MessageHeader
    body: RegisterServiceResponseBody
    def __init__(self, header: _Optional[_Union[_message_pb2.MessageHeader, _Mapping]] = ..., body: _Optional[_Union[RegisterServiceResponseBody, _Mapping]] = ...) -> None: ...

class RegisterServiceResponseBody(_message.Message):
    __slots__ = ("status", "service")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    status: _message_pb2.ResponseStatus
    service: _model_pb2.ServiceMetadata
    def __init__(self, status: _Optional[_Union[_message_pb2.ResponseStatus, _Mapping]] = ..., service: _Optional[_Union[_model_pb2.ServiceMetadata, _Mapping]] = ...) -> None: ...

class SearchServiceRequest(_message.Message):
    __slots__ = ("header", "body")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    header: _message_pb2.MessageHeader
    body: SearchServiceRequestBody
    def __init__(self, header: _Optional[_Union[_message_pb2.MessageHeader, _Mapping]] = ..., body: _Optional[_Union[SearchServiceRequestBody, _Mapping]] = ...) -> None: ...

class SearchServiceRequestBody(_message.Message):
    __slots__ = ("condition", "page")
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    condition: SearchServiceCondition
    page: _message_pb2.RequestPage
    def __init__(self, condition: _Optional[_Union[SearchServiceCondition, _Mapping]] = ..., page: _Optional[_Union[_message_pb2.RequestPage, _Mapping]] = ...) -> None: ...

class SearchServiceCondition(_message.Message):
    __slots__ = ("code", "owner")
    CODE_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    code: _code_pb2.ServiceCodeEnum
    owner: str
    def __init__(self, code: _Optional[_Union[_code_pb2.ServiceCodeEnum, str]] = ..., owner: _Optional[str] = ...) -> None: ...

class SearchServiceResponse(_message.Message):
    __slots__ = ("header", "body")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    header: _message_pb2.MessageHeader
    body: SearchServiceResponseBody
    def __init__(self, header: _Optional[_Union[_message_pb2.MessageHeader, _Mapping]] = ..., body: _Optional[_Union[SearchServiceResponseBody, _Mapping]] = ...) -> None: ...

class SearchServiceResponseBody(_message.Message):
    __slots__ = ("status", "services", "page")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    status: _message_pb2.ResponseStatus
    services: _containers.RepeatedCompositeFieldContainer[_model_pb2.ServiceMetadata]
    page: _message_pb2.ResponsePage
    def __init__(self, status: _Optional[_Union[_message_pb2.ResponseStatus, _Mapping]] = ..., services: _Optional[_Iterable[_Union[_model_pb2.ServiceMetadata, _Mapping]]] = ..., page: _Optional[_Union[_message_pb2.ResponsePage, _Mapping]] = ...) -> None: ...

class UnregisterServiceRequest(_message.Message):
    __slots__ = ("header", "body")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    header: _message_pb2.MessageHeader
    body: UnregisterServiceRequestBody
    def __init__(self, header: _Optional[_Union[_message_pb2.MessageHeader, _Mapping]] = ..., body: _Optional[_Union[UnregisterServiceRequestBody, _Mapping]] = ...) -> None: ...

class UnregisterServiceRequestBody(_message.Message):
    __slots__ = ("did", "version")
    DID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    did: str
    version: int
    def __init__(self, did: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class UnregisterServiceResponse(_message.Message):
    __slots__ = ("header", "body")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    header: _message_pb2.MessageHeader
    body: UnregisterServiceResponseBody
    def __init__(self, header: _Optional[_Union[_message_pb2.MessageHeader, _Mapping]] = ..., body: _Optional[_Union[UnregisterServiceResponseBody, _Mapping]] = ...) -> None: ...

class UnregisterServiceResponseBody(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _message_pb2.ResponseStatus
    def __init__(self, status: _Optional[_Union[_message_pb2.ResponseStatus, _Mapping]] = ...) -> None: ...
