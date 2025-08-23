import asyncio
from quickapi import QuickAPI
from quickapi.http.request import Request
from quickapi.http.response import Response
from quickapi.router import Routes
import json

users = {}

def json_response(data, status=200):
    return Response(json.dumps(data), status=status, mime_type="application/json")

routes = Routes()



@routes.get("/")
async def index(req: Request):
    return json_response({
        "title": "Eleventh",
        "subtitle": "Only 11 win",
        "links": [
            { "rel": "signup", "href": "/signup", "method": "GET" },
            { "rel": "login", "href": "/login", "method": "GET" },
        ]
    })


@routes.get("/signup")
async def signup_form(req: Request):
    return json_response({
        "message": "Signup endpoint",
        "fields": ["username", "password"],
        "links": [
            {"rel": "create", "href": "/signup", "method": "POST"},
            {"rel": "home", "href": "/", "method": "GET"}
        ]
    })

@routes.post("/signup")
async def signup(req: Request):
    data = json.loads(str(req.body))

    username = data.get("username")
    password = data.get("password")

    if username in users:
        return json_response({
            "error": f"User {username} already exists",
            "links": [{"rel": "retry", "href": "/signup", "method": "GET"}]
        }, status=400)

    users[username] = password
    return json_response({
        "message": f"Signup successful for {username}",
        "links": [{"rel": "login", "href": "/login", "method": "GET"}]
    })



# =~=~=~=~=~=~=~=~=~=~=~ Login ~=~=~=~=~=~=~=~=~=~=~=


@routes.get("/login")
async def login_form(req: Request):
    return json_response({
        "message": "Login endpoint",
        "fields": ["username", "password"],
        "links": [{"rel": "home", "href": "/", "method": "GET"}]
    })

@routes.post("/login")
async def login(req: Request):
    data = req.body
    username = data.get("username")
    password = data.get("password")
    if users.get(username) == password:
        return json_response({
            "message": f"Welcome, {username}!",
            "links": [
                {"rel": "self", "href": f"/users/{username}", "method": "GET"},
                {"rel": "logout", "href": "/logout", "method": "POST"}
            ]
        })
    return json_response({
        "error": "Invalid credentials",
        "links": [{"rel": "retry", "href": "/login", "method": "GET"}]
    }, status=401)


@routes.get("/users/{username}")
async def profile(request: Request):
    username = request["username"]

    if users.by_name(username).some():
        return json_response({"error": "User not found"}, status=404)
    else:
        return json_response({
            "username": username,
            "links": [{"rel": "home", "href": "/", "method": "GET"}]
        })



if __name__ == "__main__":
    async def demo():
        await QuickAPI().serve(routes)

    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        pass
