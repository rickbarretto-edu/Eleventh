# How to run

## 1. Start Docker Daemon

To start Docker Daemon, open Docker Desktop first.

### 2. Start server

```sh
docker-compose up --build
```

### 3. Start Clients

Open two terminals (slit mode, preferably), then run for each one:

```sh
docker exec -it chat_client1 sh
```

```sh
docker exec -it chat_client2 sh
```

For both clients, run on docker's shell:

```sh
python client.py
```