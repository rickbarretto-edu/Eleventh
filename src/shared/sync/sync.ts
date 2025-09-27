import { Hono } from "jsr:@hono/hono";

type Peer = {
    id: string,
    host: string,
    port: number
}

type SyncPayload = {
    peers?: Peer[],
    records?: { key: string, value: unknown }[]
}

export class Sync<T> {
    #database: Deno.Kv
    #self: Peer | null = null
    #peers: Peer[] = []

    private constructor(kv: Deno.Kv) {
        this.#database = kv
    }

    static async new() {
        return new Sync(await Deno.openKv())
    }

    static from<T>(kv: Deno.Kv): Sync<T> {
        return new Sync(kv)
    }

    at(peer: Peer): Sync<T> {
        this.peer(peer)
        this.#self = peer
        this.route()
        return this
    }

    private route() {
        const app = new Hono()

        app.post('/join', async (c) => {
            const peer = await c.req.json<Peer>()
            await this.peer(peer)
            return c.json({ ok: true })
        })

        app.get('/health', (c) => c.json({ ok: true }))
        app.get('/peers', (c) => c.json(this.#peers))

        app.post("/sync", async (c) => {
            const payload = await c.req.json<SyncPayload>();

            try {
                let peersJoined = 0;
                let recordsWritten = 0;

                // Sync peers if provided
                if (Array.isArray(payload.peers)) {
                    for (const p of payload.peers as Peer[]) {
                        if (!p || !p.host || !p.port) continue;
                        if (!this.isPeerRegistered(p)) {
                            this.#peers.push(p);
                            peersJoined++;
                        }
                    }
                }

                // Sync KV records if provided
                if (Array.isArray(payload.records)) {
                    for (const rec of payload.records) {
                        if (!rec || !Array.isArray(rec.key)) continue;
                        await this.#database.set(rec.key, rec.value);
                        recordsWritten++;
                    }
                }

                return c.json({
                    ok: true,
                    peersAdded: peersJoined,
                    recordsWritten,
                    peers: this.#peers
                })
            } catch (err) {
                return c.json({ ok: false, error: String(err) }, 500);
            }
        })

        Deno.serve({
            hostname: this.self!.host,
            port: this.self!.port
        }, app.fetch)
    }

    // Register a peer, used internally on routes
    private async peer(peer: Peer) {
        if (this.isPeerRegistered(peer)) {
            throw new Error(`Peer ${peer.host}:${peer.port} already registered`)
        }

        this.#peers.push(peer)

        const targets = this.#peers.filter(p => p != this.self)
        const body = JSON.stringify({ peers: this.#peers })

        await Promise.allSettled(targets.map(t =>
            fetch(`http://${t.host}:${t.port}/sync`, {
                method: "POST",
                headers: { "content-type": "application/json" },
                body
            }).catch(() => undefined)
        ))
    }

    private isPeerRegistered(peer: Peer) {
        return this.#peers.find(p => p.host === peer.host && p.port === peer.port);
    }

    joinTo(peer: Peer) {
        fetch(`http://${peer.host}:${peer.port}/join`, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify(this.self)
        }).catch(() => undefined)
    }

    get peers() {
        return this.#peers
    }

    get self() {
        return this.#self!
    }

}