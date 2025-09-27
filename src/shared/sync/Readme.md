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