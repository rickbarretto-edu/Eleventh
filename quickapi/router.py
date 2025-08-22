from __future__ import annotations

from typing import Awaitable, Callable, Self
import attrs

from quickapi.http.request import Request, Method, Target
from quickapi.http.response import Response, Status


type Action = Callable[[Request], Awaitable[Response]]

@attrs.frozen
class Endpoints:
    each: dict[tuple[Method, Target], Action] = attrs.field(factory=dict)

    def of(self, method: Method, path: Target) -> Action:
        return self.each[(method, path)]
    
    def add(self, method: Method, path: Target, action: Action) -> None:
        self.each[(method, path)] = action

    def __or__(self, other: Endpoints) -> Self:
        return attrs.evolve(self, each=self.each | other.each)


@attrs.frozen
class Routes:
    endpoints: Endpoints = Endpoints()

    def at(self, path: str, method: str) -> Callable[[Action], Action]:
        def decorator(func: Action) -> Action:
            self.endpoints.add(Method(method), Target(path), func)
            return func
        return decorator

    def __or__(self, routes: Routes) -> Self:

        return attrs.evolve(self, endpoints=self.endpoints | routes.endpoints)

    def __getattr__(self, name: str) -> Callable[[str], Callable[[Action], Action]]:
        def wrapper(path: str) -> Callable[[Action], Action]:
            return self.at(path, name.upper())
        return wrapper

    async def __call__(self, request: Request) -> Response:
        print(self.endpoints.each)
        try:
            action = self.endpoints.of(request.method, request.target)
            return await action(request)
        except KeyError:
            return Response("404, Not Found!", status=Status.NotFound)
    
