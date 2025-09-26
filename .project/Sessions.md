# PBL Session Summaries

## Week 1 — 23/09/2025

**Facts**

* The game must move to a distributed system with multiple servers.
* No single point of failure — the system should keep running even if one server fails.
* Use **Docker** for servers and clients.
* **Server–Server:** REST API.
* **Server–Client:** Publisher–Subscriber model.
* Card packs must be managed fairly and without duplication.
* Matches should work across servers (1×1 duels).
* The system must be tested for concurrency and failures.

**Ideas**

* Each game server runs in Docker, handles local matches, connects to clients (pub-sub), and communicates with other servers (REST).
* Pub-Sub: topics for matches, lobby, and inventory/trade.
* REST: endpoints for matchmaking, syncing, and heartbeat.
* Matchmaking: handshake + confirmation, fallback if a server fails.
* Fault tolerance: heartbeats, retries, two-phase commit, and replaying events.

**Questions**

* What is a REST API?
* What is pub-sub and which tech should we use (WebSockets, MQTT, NATS)?
* How do clients log in and join matches?
* How do we identify matches (IDs)?
* What is the message format (JSON)?
* What is idempotency and how do we avoid duplicates?
* How to avoid giving the same card pack twice?
* What happens if a server crashes mid-match?
* How do servers find each other?
* What logs do we need?

**Goals**

* Study the **Byzantine Generals Problem** (consensus and fault tolerance).
* Learn and apply **pub-sub** for Server–Client communication. (Development)
* Define topics, message format, and events.
