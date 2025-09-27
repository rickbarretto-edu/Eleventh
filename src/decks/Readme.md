# Deck Management Service

This directory provides a deck management service that works synced across containers, by using Sync.

## Features

- Deno server: `src/decks/server.ts`
- KV-backed deck so multiple container replicas share the same deck state
- Dockerfile and docker-compose to run locally and scale replicas

## Card format

```ts
type Card = {
  name: string
  position: 'atk' | 'mid' | 'def' | 'gk'
  power: number
}
```

## Run locally (requires Deno)

```
deno run --allow-net --allow-env src/decks/server.ts
```

## Run with Docker Compose (build + local Redis)

```
docker compose up --build
# to scale replicas:
docker compose up --build --scale deck-server=3
```

## Endpoints

- `GET /claim`: returns up to 5 cards popped from the shared deck as JSON array
- `GET /health`: returns { ok: true }
