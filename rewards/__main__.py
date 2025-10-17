"""Rewarding System

This subsystem generates the rewards used in Eleventh
and does not store anything.

This service is used with lower frequency,
and thus, there is no need for any complex algorithm.

Leader ellection happens via Bully algorithm, so the higest ID will be choosen. 
Since this doesn't need data consistency, the follower just redirects the generated deck to the user.

The other followers will only work as a backup service,
so when the highest server goes down, the next highest one takes control.
"""

from fastapi.applications import FastAPI

from rewards.routes import router


app = FastAPI()
app.include_router(router)