# Eleventh

<p align="center">Only 11 wins.</p>

**Eleventh** is a turn-based card game inspired by FIFA’s Ultimate Team cards and the strategic style of Soccer Manager.
Players build their own dream team using collectible cards, manage tactics, and compete in tactical duels against other managers. 


## Routine Tests

```sh
$ cargo run -p server
```

### Account Creation

```sh
$ curl http://127.0.0.1:8080/accounts/
$ curl -X POST http://127.0.0.1:8080/accounts/create/ -d '{"username": "Rick", "password": "123456"}'
$ curl -X POST http://127.0.0.1:8080/accounts/login/ -d '{"username": "Rick", "password": "123456"}'
```