from typing import Optional, Dict, Any, List, Callable, Union, Tuple, TypeVar, Literal, TypedDict, Type
from enum import Enum
import requests
HttpMethod = Literal['GET', 'POST', 'PUT',
                     'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
T = TypeVar('T')


class EndpointConfig(TypedDict):
    name: Optional[str]
    method: HttpMethod
    path: str
    params: List[str]
    description: Optional[str]


class RetryConfig(TypedDict, total=False):
    retries: int
    connect: int
    read: int
    status: int
    backoff_factor: float
    status_forcelist: List[int]
    allowed_methods: List[HttpMethod]
    raise_on_status: bool
    respect_retry_after_header: bool


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
