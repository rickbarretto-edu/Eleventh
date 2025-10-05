"""Accounts Service.

At A Glance
-----------

Start the service with:

        poetry run uvicorn eleventh.services.accounts.__main__:app --host 127.0.0.1 --port 8001 --reload

To manually create a user, use `curl` or similar:

        curl -X POST "http://localhost:8001/accounts/signup/" -H "Content-Type: application/json" -d '{"email": "<email>", "username": "<username>", "password": "<password>"}'

To manually authenticate a user, use `curl` or similar:

        curl -X POST "http://localhost:8001/accounts/login/" -H "Content-Type: application/json" -d '{"email": "<email>", "password": "<password>"}'
"""

from fastapi import FastAPI

from eleventh.services.accounts import route

app = FastAPI()
app.include_router(route)