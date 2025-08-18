


from typing import Awaitable, Callable
from weakref import KeyedRef
import attrs

from quickapi.rtp.request import Request, Method, Path
from quickapi.rtp.response import PlainText, Response, Status


type Action = Callable[[Request], Awaitable[Response]]

@attrs.frozen
class Endpoints:
    each: dict[tuple[Method, Path], Action] = attrs.field(factory=dict)

    def of(self, method: Method, path: Path) -> Action:
        return self.each[(method, path)]
    
    def add(self, method: Method, path: Path, action: Action) -> None:
        self.each[(method, path)] = action


@attrs.frozen
class Routes:
    _endpoints: Endpoints

    def at(self, path: str, method: str) -> Callable[[Action], Action]:
        def decorator(func: Action) -> Action:
            self._endpoints.add(Method(method), Path(path), func)
            return func
        return decorator

    def __getattr__(self, name: str) -> Callable[[str], Callable[[Action], Action]]:
        def wrapper(path: str) -> Callable[[Action], Action]:
            return self.at(path, name.upper())
        return wrapper

    async def __call__(self, request: Request) -> Response:
        print(self._endpoints.each)
        try:
            action = self._endpoints.of(request.method, request.path)
            return await action(request)
        except KeyError:
            return Response(Status.NotFound, body=PlainText("404 Not Found"))
    
