import asyncio
from quickapi import QuickAPI
from quickapi.http.request import Request
from quickapi.http.response import HttpResponse
from quickapi.http.response.status import Status
from quickapi.router import Routes
import json

users = {}

def json_response(data, status=200):
    return HttpResponse(json.dumps(data), status=status, mime_type="application/json")

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
        return JsonResponse({
            "error": f"User {username} already exists",
            "links": [{"rel": "retry", "href": "/signup", "method": "GET"}]
        }).bad_request()

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

    if users.by_name(username).exact().password == password:
        return JsonResponse({
            "message": f"Welcome, {username}!",
            "links": [
                {"rel": "self", "href": f"/users/{username}", "method": "GET"},
                {"rel": "logout", "href": "/logout", "method": "POST"}
            ]
        })
    else:
        return JsonResponse({
            "error": "Invalid credentials",
            "links": [{"rel": "retry", "href": "/login", "method": "GET"}]
        }).invalid_credential()


@routes.get("/users/{username}")
async def profile(request: Request):
    username = request["username"]

    if users.by_name(username).some():
        return JsonResponse({"error": "User not found"}).not_found()
    else:
        return JsonResponse({
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
