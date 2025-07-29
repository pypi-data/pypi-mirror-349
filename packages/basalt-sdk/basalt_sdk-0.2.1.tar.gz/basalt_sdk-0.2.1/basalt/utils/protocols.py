from typing import Any, Optional, Protocol, Hashable, Tuple, TypeVar, Dict, Mapping, Literal
from .dtos import GetResult, DescribeResult, ListResult

from ..ressources.monitor.monitorsdk_types import IMonitorSDK

Input = TypeVar('Input')
Output = TypeVar('Output')

class ICache(Protocol):
    def get(self, key: Hashable) -> Optional[Any]: ...
    def put(self, key: Hashable, value: Any, duration: int) -> None: ...

class IEndpoint(Protocol[Input, Output]):
    def prepare_request(self, dto: Optional[Input] = None) -> Dict[str, Any]: ...
    def decode_response(self, response: Any) -> Tuple[Optional[Exception], Optional[Output]]: ...

class IApi(Protocol):
    def invoke(self,endpoint: IEndpoint[Input, Output], dto: Optional[Input] = None) -> Tuple[Optional[Exception], Optional[Output]]: ...

class INetworker(Protocol):
    def fetch(self,
              url: str,
              method: str,
              body: Optional[Any] = None,
              params: Optional[Mapping[str, str]] = None,
              headers: Optional[Mapping[str, str]] = None
            ) -> Tuple[Optional[Exception], Optional[Output]]: ...

class IPromptSDK(Protocol):
    def get(self, slug: str, tag: Optional[str] = None, version: Optional[str] = None, variables: Dict[str, str] = {}, cache_enabled: bool = True) -> GetResult: ...
    def describe(self, slug: str, tag: Optional[str] = None, version: Optional[str] = None) -> DescribeResult: ...
    def list(self, feature_slug: Optional[str] = None) -> ListResult: ...

class IBasaltSDK(Protocol):
    @property
    def prompt(self) -> IPromptSDK: ...
    @property
    def monitor(self) -> IMonitorSDK: ...

class ILogger:
    def warn(self, message: str): ...
    def info(self, message: str): ...
    def error(self, message: str): ...


LogLevel = Literal["all", "warning", "none"]

