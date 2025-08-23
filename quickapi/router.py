from __future__ import annotations

import re
import attrs
from typing import Awaitable, Callable, Self

from quickapi.http.request import Request, Method, Target
from quickapi.http.response import HttpResponse, Status

type Action = Callable[[Request], Awaitable[HttpResponse]]

@attrs.frozen
class RouteEntry:
    pattern: re.Pattern
    parameters: list[str]
    action: Action

@attrs.frozen
class Endpoints:
    entries: list[RouteEntry] = attrs.field(factory=list)

    def add(self, method: Method, path: str, action: Action) -> None:
        parameters = re.findall(r"{(\w+)}", path)
        path = re.sub(r"{\w+}", r"([^/]+)", path)
        pattern = re.compile(f"^{path}$")
        self.entries.append(RouteEntry(pattern, parameters, action))

    def match(self, method: Method, target: str) -> tuple[Action, dict[str, str]] | None:
        for entry in self.entries:
            if match := entry.pattern.match(target):
                params = dict(zip(entry.parameters, match.groups()))
                return entry.action, params
        return None

    def __or__(self, other: Endpoints) -> Self:
        return attrs.evolve(self, entries=self.entries + other.entries)


@attrs.frozen
class Routes:
    endpoints: Endpoints = Endpoints()

    def at(self, path: str, method: str) -> Callable[[Action], Action]:
        def decorator(func: Action) -> Action:
            self.endpoints.add(Method(method), path, func)
            return func
        return decorator

    def __getattr__(self, name: str) -> Callable[[str], Callable[[Action], Action]]:
        def wrapper(path: str) -> Callable[[Action], Action]:
            return self.at(path, name.upper())
        return wrapper

    async def __call__(self, request: Request) -> HttpResponse:
        if result := self.endpoints.match(request.method, str(request.target)):
            action, params = result
            return await action(request)

        return HttpResponse("404, Not Found!", status=Status.NotFound)
