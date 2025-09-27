# Sync

## Running it manually

Start each server manually:

```sh
deno run --unstable-kv -A cli.ts s1 127.0.0.1 4000
```

```sh
deno run --unstable-kv -A cli.ts s2 127.0.0.1 4001
```

```sh
deno run --unstable-kv -A cli.ts s3 127.0.0.1 4002
```

Check their health manually:

```sh
$ curl -X GET 127.0.0.1:4000/health                                                                           
{"ok":true}
$ curl -X GET 127.0.0.1:4001/health
{"ok":true}
$ curl -X GET 127.0.0.1:4002/health
{"ok":true}
```

Join each server manually:

```sh
$ curl -X POST 127.0.0.1:4000/join -H "content-type: application/json" -d '{"id":"s2","host":"127.0.0.1","port":4001}'                                                   
{"ok":true}
$ curl -X POST 127.0.0.1:4000/join -H "content-type: application/json" -d '{"id":"s3","host":"127.0.0.1","port":4002}'
{"ok":true}
```

Check if peers are synced:

```sh
$ curl -X GET 127.0.0.1:4000/peers                                   
[{"id":"s1","host":"127.0.0.1","port":4000},{"id":"s2","host":"127.0.0.1","port":4001},{"id":"s3","host":"127.0.0.1","port":4002}]
$ curl -X GET 127.0.0.1:4001/peers                                                                            
[{"id":"s2","host":"127.0.0.1","port":4001},{"id":"s1","host":"127.0.0.1","port":4000},{"id":"s3","host":"127.0.0.1","port":4002}]
$ curl -X GET 127.0.0.1:4002/peers                                                                            
[{"id":"s3","host":"127.0.0.1","port":4002},{"id":"s1","host":"127.0.0.1","port":4000},{"id":"s2","host":"127.0.0.1","port":4001}]
```

## Running on REPL

```ts
$ deno repl --unstable-kv
Deno 2.2.8
exit using ctrl+d, ctrl+c, or close()
> import { Sync } from "./Sync.ts"
✅ Granted read access to "...\eleventh\src\shared\sync\Sync.ts".
undefined
```

Defining new peers:

```ts
> const p1 = { host: "localhost", port: 4001, id: "Node 1" }
undefined
> const p2 = { host: "localhost", port: 4002, id: "Node 2" }
undefined
> const p3 = { host: "localhost", port: 4003, id: "Node 3" }
undefined
> const n1 = Sync.at(p1)
✅ Granted net access to "localhost:4001".
Listening on http://[::1]:4001/
undefined
> const n2 = Sync.at(p2)
✅ Granted net access to "localhost:4002".
Listening on http://[::1]:4002/
undefined
> const n3 = Sync.at(p3)
✅ Granted net access to "localhost:4003".
Listening on http://[::1]:4003/
undefined
```

Checking clusters:

```ts
> n1.peers
[ { host: "localhost", port: 4001, id: "Node 1" } ]
> n2.peers
[ { host: "localhost", port: 4002, id: "Node 2" } ]
> n3.peers
[ { host: "localhost", port: 4003, id: "Node 3" } ]
> n1.cluster()
undefined
> Node 1@localhost:4001: ok
> n2.cluster()
undefined
> Node 2@localhost:4002: ok
> n3.cluster()
undefined
> Node 3@localhost:4003: ok
```

Joining Node 2 to Node 1:

```ts
> n2.join(p1)
undefined
> n1.peers
[
  { host: "localhost", port: 4001, id: "Node 1" },
  { host: "localhost", port: 4002, id: "Node 2" }
]
> n1.cluster
[Function: cluster]
> n1.cluster()
undefined
> Node 1@localhost:4001: ok
Node 2@localhost:4002: ok

undefined
> n2.cluster()
undefined
> Node 2@localhost:4002: ok
Node 1@localhost:4001: ok

undefined
> n3.cluster()
undefined
> Node 3@localhost:4003: ok

undefined
```

Joining Node 3 to Cluster:

```ts
> n3.join(p2)
undefined
> n2.cluster()
undefined
> Node 2@localhost:4002: ok
Node 1@localhost:4001: ok
Node 3@localhost:4003: ok

undefined
> n1.cluster()
undefined
> Node 1@localhost:4001: ok
Node 2@localhost:4002: ok
Node 3@localhost:4003: ok

undefined
> n3.cluster()
undefined
> Node 3@localhost:4003: ok
Node 2@localhost:4002: ok
Node 1@localhost:4001: ok

undefined
>
```