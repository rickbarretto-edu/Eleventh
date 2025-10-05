"""Logging Service.

At a Glance
-----------

Start the service with:

        poetry run uvicorn eleventh.services.logging.__main__:app --host 127.0.0.1 --port 8001 --reload

Now, open your browser to `http://localhost:8001/log/ui` to see the logs UI.

To manually publish a log message, use `curl` or similar:

        curl -X POST "http://localhost:8001/log/" -d '"Your log message here"'
"""

from fastapi import FastAPI

from eleventh.services.logging import api

app = FastAPI()
app.include_router(api.route)