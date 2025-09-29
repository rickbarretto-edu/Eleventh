import { newHttpBatchRpcResponse, newWebSocketRpcSession, RpcTarget } from "@capnweb"
import { ClusterApi } from "./api.ts"
import { Peer } from "./models.ts";

const samePeers = (a: Peer, b: Peer): boolean => a.host === b.host && a.port === b.port

export class ClusterServer extends RpcTarget implements ClusterApi {
    #current: Peer
    #others: Peer[] = []

    constructor(current: Peer) {
        super()
        this.#current = current
    }

    async #broadcast(fn: (cluster: ClusterApi) => Promise<void> | void): Promise<void> {
        const peers = this.#others.slice()

        await Promise.allSettled(peers.map(async (peer) => {
            if (this.#isSelf(peer)) return

            const url = `ws://${peer.host}:${peer.port}/api`
            try {
                // Open a WebSocket RPC session to the peer
                const api = newWebSocketRpcSession<ClusterApi>(url)

                try {
                    // The RPC stub returned by capnweb wraps remote values in promises/stubs.
                    // We call the provided function with the stub and await any promises it returns.
                    const result = fn(api as unknown as ClusterApi)
                    if (result instanceof Promise) await result
                } finally {
                    // Dispose/close the session if supported. Use unknown cast to avoid `any`.
                    try {
                        ;(api as unknown as { [Symbol.dispose]?: () => void })[Symbol.dispose]?.()
                    } catch (_e) {
                        // ignore disposal errors
                    }
                }
            } catch (err) {
                console.warn(`Failed to broadcast to ${peer.host}:${peer.port}:`, err)
            }
        }))
    }

    #isSelf(peer: Peer): boolean {
        return samePeers(this.#current, peer)
    }

    #exists(peer: Peer): boolean {
        const peers = this.#others.concat(this.#current)
        return peers.some(p => samePeers(p, peer))
    }

    async attach(peer: Peer): Promise<void> {
        if (this.#isSelf(peer)) {
            console.warn(`Refusing to attach self: ${peer.host}:${peer.port}`)
            return
        }

        if (this.#exists(peer)) {
            console.warn(`Peer already exists: ${peer.host}:${peer.port}`)
            return
        }

        this.#others.push(peer)
        await this.#broadcast((cluster) => cluster.attach(peer))
        console.log(`Peer attached: ${peer.host}:${peer.port}`)
    }

    async disconnect(peer: Peer): Promise<void> {
        if (this.#isSelf(peer)) {
            console.warn(`Refusing to disconnect self: ${peer.host}:${peer.port}`)
            return
        }

        this.#others = this.#others.filter(p => !samePeers(p, peer))
        await this.#broadcast((cluster) => cluster.disconnect(peer))
        console.log(`Peer disconnected: ${peer.host}:${peer.port}`)
    }

    get peers(): Peer[] {
        return this.#others.concat(this.#current);
    }
}

export function serve(peer: Peer): AbortController {
    const controller = new AbortController()

    Deno.serve({ hostname: peer.host, port: peer.port, signal: controller.signal }, async (req) => {
        const url = new URL(req.url);
        if (url.pathname === "/api") {
            if (req.headers.get("upgrade") === "websocket") {
                const { socket, response } = Deno.upgradeWebSocket(req);
                socket.addEventListener("open", () => {
                    newWebSocketRpcSession(socket, new ClusterServer(peer));
                });
                return response;
            } else {
                const response = await newHttpBatchRpcResponse(req, new ClusterServer(peer));
                response.headers.set("Access-Control-Allow-Origin", "*");
                return response;
            }
        }

        return new Response("Not Found", { status: 404 });
    })

    return controller
}