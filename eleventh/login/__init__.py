import json

from eleventh.login.model import UserLogin
from quickapi import QuickAPI
from quickapi.http.request import Request
from quickapi.http.request.target import JsonValue
from quickapi.http.response import JsonResponse
from quickapi.router import Routes

from .repository import Users, UsersInSQLite

users: Users = UsersInSQLite("data/users.db")
routes = Routes()


def from_json(request: Request) -> JsonValue:
    return json.loads(str(request.body))


@routes.get("/")
async def index(request: Request):
    return JsonResponse({
        "title": "Eleventh",
        "subtitle": "Only 11 win",
        "links": [
            { "rel": "signup", "href": "/signup", "method": "GET" },
            { "rel": "login", "href": "/login", "method": "GET" },
        ]
    })


# =~=~=~=~=~=~=~=~=~=~=~ SignUp ~=~=~=~=~=~=~=~=~=~=~=


@routes.get("/signup")
async def signup_form(request: Request) -> JsonResponse:
    return JsonResponse({
        "message": "Create New Account",
        "fields": ["username", "password"],
        "links": [
            {"rel": "create", "href": "/signup", "method": "POST"},
            {"rel": "home", "href": "/", "method": "GET"}
        ]
    })

@routes.post("/signup")
async def signup(request: Request) -> JsonResponse:
    data = from_json(request)

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str): 
        return JsonResponse({
            "error": f"username must be a string",
            "links": [{"rel": "retry", "href": "/signup", "method": "GET"}]
        }).BadRequest

    if user_id := users.by_name(username):
        return JsonResponse({
            "message": f"Signup successful for {username}",
            "token": str(user_id),
            "links": [{"rel": "login", "href": "/login", "method": "GET"}]
        })
    else:
        return JsonResponse({
            "error": f"User {username} already exists",
            "links": [{"rel": "retry", "href": "/signup", "method": "GET"}]
        }).BadRequest


# =~=~=~=~=~=~=~=~=~=~=~ Login ~=~=~=~=~=~=~=~=~=~=~=


@routes.get("/login")
async def login_form(req: Request):
    return JsonResponse({
        "message": "Login endpoint",
        "fields": ["username", "password"],
        "links": [{"rel": "home", "href": "/", "method": "GET"}]
    })

@routes.post("/login")
async def login(request: Request):
    data = from_json(request)
    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return JsonResponse({
            "error": "Username and Password must be strings.",
            "links": [{"rel": "retry", "href": "/login", "method": "GET"}]
        }).BadRequest

    if user_id := users.auth(UserLogin(username, password)):
        return JsonResponse({
            "message": f"Welcome, {username}!",
            "links": [
                {"rel": "self", "href": f"/users/{user_id}", "method": "GET"},
                {"rel": "logout", "href": "/logout", "method": "POST"}
            ]
        })
    else:
        return JsonResponse({
            "error": "Invalid credentials",
            "links": [{"rel": "retry", "href": "/login", "method": "GET"}]
        }).BadRequest


@routes.get("/users/{username}")
async def profile(request: Request):
    username = request["username"]

    if not users.by_name(username):
        return JsonResponse({"error": "User not found"}).NotFound
    else:
        return JsonResponse({
            "username": username,
            "links": [{"rel": "home", "href": "/", "method": "GET"}]
        })


if __name__ == "__main__":

    import asyncio

    async def demo():
        await QuickAPI().serve(routes)

    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        pass
